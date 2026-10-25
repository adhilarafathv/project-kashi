
from flask import Flask, render_template, request, redirect, url_for
from db import get_db_connection
from decimal import Decimal, InvalidOperation
import secrets
import string

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

ACCOUNT_TYPES = {"Saving", "Current", "Salary"}


def load_account(cursor, account_id):
    cursor.execute("""
        SELECT
            a.AccountID,
            a.AccountNumber,
            a.AccountType,
            a.OpeningDate,
            a.Balance,
            a.Status,
            c.FirstName,
            c.LastName,
            c.CustomerID,
            b.BranchName
        FROM ACCOUNT a
        JOIN ACCOUNT_HOLDER ah ON a.AccountID = ah.AccountID
        JOIN CUSTOMER c ON ah.CustomerID = c.CustomerID
        JOIN BRANCH b ON a.BranchID = b.BranchID
        WHERE a.AccountID = %s
        LIMIT 1
    """, (account_id,))

    return cursor.fetchone()


def render_account_page(cursor, account_id, error=None, success=None):
    account = load_account(cursor, account_id)

    if account is None:
        return "Account not found.", 404

    cursor.execute("""
        SELECT
            TransactionID,
            TransactionType,
            Amount,
            TransactionDate,
            Description,
            ReferenceNumber,
            TransactionStatus
        FROM BANK_TRANSACTION
        WHERE AccountID = %s
        ORDER BY TransactionDate DESC, TransactionID DESC
    """, (account_id,))

    transactions = cursor.fetchall()

    return render_template(
        "account_detail.html",
        account=account,
        transactions=transactions,
        error=error,
        success=success
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/customers")
def customers():
    connection = get_db_connection()

    if connection is None:
        return "Database connection failed.", 500

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT CustomerID, FirstName, LastName, Mobile, City
            FROM CUSTOMER
            ORDER BY CustomerID
        """)

        return render_template(
            "customers.html",
            customers=cursor.fetchall()
        )

    finally:
        cursor.close()
        connection.close()


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()
    dob = request.form.get("dob", "").strip()
    mobile = request.form.get("mobile", "").strip()
    email = request.form.get("email", "").strip() or None
    city = request.form.get("city", "").strip() or None

    if not all([first_name, last_name, dob, mobile]):
        return (
            "First name, last name, date of birth and mobile are required.",
            400
        )

    connection = get_db_connection()

    if connection is None:
        return "Database connection failed.", 500

    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO CUSTOMER
                (FirstName, LastName, DateOfBirth, Mobile, Email, City)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, dob, mobile, email, city))

        connection.commit()
        return redirect(url_for("customers"))

    except Exception:
        connection.rollback()

        return (
            "Could not register customer. Check the form and ensure "
            "the mobile number and email are not already registered.",
            400
        )

    finally:
        cursor.close()
        connection.close()


@app.route("/accounts/create", methods=["GET", "POST"])
def create_account():
    connection = get_db_connection()

    if connection is None:
        return "Database connection failed.", 500

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT CustomerID, FirstName, LastName
            FROM CUSTOMER
            ORDER BY CustomerID
        """)
        customer_list = cursor.fetchall()

        cursor.execute("""
            SELECT BranchID, BranchName
            FROM BRANCH
            ORDER BY BranchID
        """)
        branch_list = cursor.fetchall()

        if request.method == "GET":
            return render_template(
                "create_account.html",
                customers=customer_list,
                branches=branch_list
            )

        customer_id = request.form.get("customer_id", "")
        branch_id = request.form.get("branch_id", "")
        account_type = request.form.get("account_type", "")

        if account_type not in ACCOUNT_TYPES:
            return "Invalid account type.", 400

        if not any(
            str(customer["CustomerID"]) == customer_id
            for customer in customer_list
        ):
            return "Please select a valid customer.", 400

        if not any(
            str(branch["BranchID"]) == branch_id
            for branch in branch_list
        ):
            return "Please select a valid branch.", 400

        # Generate a unique 12-digit account number.
        while True:
            account_number = "".join(
                secrets.choice(string.digits) for _ in range(12)
            )

            cursor.execute(
                "SELECT AccountID FROM ACCOUNT WHERE AccountNumber = %s",
                (account_number,)
            )

            if cursor.fetchone() is None:
                break

        cursor.execute("""
            INSERT INTO ACCOUNT
                (AccountNumber, AccountType, OpeningDate,
                 Balance, Status, BranchID)
            VALUES (%s, %s, CURRENT_DATE, 0.00, 'Active', %s)
        """, (account_number, account_type, branch_id))

        account_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO ACCOUNT_HOLDER
                (CustomerID, AccountID, HolderSince, HolderType)
            VALUES (%s, %s, CURRENT_DATE, 'Primary')
        """, (customer_id, account_id))

        connection.commit()

        return redirect(
            url_for("account_details", account_id=account_id)
        )

    except Exception:
        connection.rollback()

        return (
            "Could not create the account. Check the selected customer, "
            "branch and form values.",
            400
        )

    finally:
        cursor.close()
        connection.close()


@app.route("/accounts")
def accounts():
    connection = get_db_connection()

    if connection is None:
        return "Database connection failed.", 500

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                a.AccountID,
                a.AccountNumber,
                a.AccountType,
                a.Balance,
                a.Status,
                c.FirstName,
                c.LastName,
                b.BranchName
            FROM ACCOUNT a
            JOIN ACCOUNT_HOLDER ah ON a.AccountID = ah.AccountID
            JOIN CUSTOMER c ON ah.CustomerID = c.CustomerID
            JOIN BRANCH b ON a.BranchID = b.BranchID
            ORDER BY a.AccountID
        """)

        return render_template(
            "accounts.html",
            accounts=cursor.fetchall()
        )

    finally:
        cursor.close()
        connection.close()


@app.route("/accounts/<int:account_id>", methods=["GET", "POST"])
def account_details(account_id):
    connection = get_db_connection()

    if connection is None:
        return "Database connection failed.", 500

    cursor = connection.cursor(dictionary=True)

    if request.method == "GET":
        try:
            # Read the confirmation message after a successful redirect.
            success = request.args.get("success")

            return render_account_page(
                cursor,
                account_id,
                success=success
            )

        finally:
            cursor.close()
            connection.close()

    try:
        transaction_type = request.form.get("transaction_type", "")
        description = request.form.get("description", "").strip() or None

        if transaction_type not in {"DEPOSIT", "WITHDRAWAL"}:
            return render_account_page(
                cursor,
                account_id,
                error="Invalid transaction type."
            ), 400

        try:
            amount_text = request.form.get("amount", "").strip()
            amount = Decimal(amount_text)

            if not amount.is_finite() or amount <= 0:
                raise InvalidOperation

            if amount.as_tuple().exponent < -2:
                raise InvalidOperation

            amount = amount.quantize(Decimal("0.01"))

        except (InvalidOperation, ValueError, AttributeError):
            return render_account_page(
                cursor,
                account_id,
                error=(
                    "Enter a valid amount greater than zero, "
                    "with at most two decimal places."
                )
            ), 400

        # Start a transaction and lock the account row.
        # This protects the balance from concurrent updates.
        connection.start_transaction()

        cursor.execute("""
            SELECT Balance, Status
            FROM ACCOUNT
            WHERE AccountID = %s
            FOR UPDATE
        """, (account_id,))

        locked_account = cursor.fetchone()

        if locked_account is None:
            connection.rollback()
            return "Account not found.", 404

        if locked_account["Status"] != "Active":
            connection.rollback()

            return render_account_page(
                cursor,
                account_id,
                error="Transactions are allowed only on Active accounts."
            ), 400

        current_balance = Decimal(str(locked_account["Balance"]))

        if transaction_type == "WITHDRAWAL" and amount > current_balance:
            connection.rollback()

            return render_account_page(
                cursor,
                account_id,
                error="Insufficient balance. Withdrawal was not processed."
            ), 400

        if transaction_type == "DEPOSIT":
            new_balance = current_balance + amount
        else:
            new_balance = current_balance - amount

        cursor.execute("""
            UPDATE ACCOUNT
            SET Balance = %s
            WHERE AccountID = %s
        """, (new_balance, account_id))

        reference_number = "KASHI-" + secrets.token_hex(6).upper()

        cursor.execute("""
            INSERT INTO BANK_TRANSACTION
                (AccountID, TransactionType, Amount, Description,
                 ReferenceNumber, TransactionStatus)
            VALUES (%s, %s, %s, %s, %s, 'Success')
        """, (
            account_id,
            transaction_type,
            amount,
            description,
            reference_number
        ))

        # Save the balance update and transaction record together.
        connection.commit()

        message = (
            f"{transaction_type.title()} successful. "
            f"Reference: {reference_number}"
        )

        # Redirect after POST so refreshing the page won't repeat
        # the same deposit or withdrawal.
        return redirect(
            url_for(
                "account_details",
                account_id=account_id,
                success=message
            )
        )

    except Exception:
        connection.rollback()

        return render_account_page(
            cursor,
            account_id,
            error="The transaction failed. No balance change was saved."
        ), 500

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)
