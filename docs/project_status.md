# Project KASHI — Final Project Status

**Last Updated:** October 27, 2026

## 1. Project Overview

Project KASHI is an educational Banking Management System developed to demonstrate relational database design, SQL programming, database integrity, transaction processing, and integration between a web application and a relational database.

### Technology Stack
- **Frontend:** HTML and CSS
- **Backend:** Python and Flask
- **Database:** MySQL 8.0
- **Database connector:** `mysql-connector-python`
- **Version control:** Git and GitHub

## 2. Project Structure

```text
Project Kashi/
├── backend/
│   ├── app.py
│   ├── db.py
│   └── test_db.py
├── database/
│   ├── schema.sql
│   ├── queries.sql
│   ├── views.sql
│   ├── functions.sql
│   ├── procedures.sql
│   └── triggers.sql
├── docs/
│   ├── er_diagram.md
│   └── project_status.md
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
├── templates/
│   ├── index.html
│   ├── customers.html
│   ├── register.html
│   ├── create_account.html
│   ├── accounts.html
│   └── account_detail.html
├── .gitignore
├── README.md
└── requirements.txt
```

## 3. Database Design

The database is named `project_kashi`.

Six core tables have been designed and implemented:

1. `CUSTOMER` — stores customer details.
2. `BRANCH` — stores bank branch information.
3. `EMPLOYEE` — stores employee details and branch assignments.
4. `ACCOUNT` — stores account numbers, types, balances, statuses, and branch assignments.
5. `ACCOUNT_HOLDER` — links customers and accounts.
6. `BANK_TRANSACTION` — records account transactions.

### Keys and Constraints
- Primary keys uniquely identify records.
- Foreign keys maintain relationships between related tables.
- Unique constraints prevent duplicate values in designated columns.
- `ACCOUNT_HOLDER` uses a composite primary key consisting of `CustomerID` and `AccountID`.
- `NOT NULL` constraints enforce required fields.
- Monetary values use `DECIMAL` data types.
- Account and transaction records reference their associated branches and accounts through foreign keys.

## 4. Database Relationships

- **CUSTOMER–ACCOUNT: M:N**, implemented using `ACCOUNT_HOLDER`.
- **BRANCH–EMPLOYEE: 1:N**, implemented using `EMPLOYEE.BranchID`.
- **BRANCH–ACCOUNT: 1:N**, implemented using `ACCOUNT.BranchID`.
- **ACCOUNT–BANK_TRANSACTION: 1:N**, implemented using `BANK_TRANSACTION.AccountID`.

The optional loan and loan-payment modules are excluded from the current implementation.

## 5. Completed Application Features

### Customer Management
- Customer registration.
- Customer listing.
- Storage and retrieval of customer information.

### Account Management
- Account creation and listing.
- Association of accounts with customers and branches.
- Individual account detail pages.
- Display of account type, number, balance, status, branch, and transaction history.

### Banking Transactions
- Deposits and withdrawals.
- Recording of transaction amounts, types, descriptions, reference numbers, timestamps, and statuses.
- Automatic balance updates through the application workflow.
- Transaction history for individual accounts.

### Validation and Transaction Safety
- Parameterized SQL queries for database operations.
- Validation of transaction type and amount.
- Rejection of nonpositive transaction amounts.
- Prevention of withdrawals exceeding the available balance.
- Restriction of transactions to accounts with `Active` status.
- Use of database transactions to group balance updates and transaction-record insertion.
- Rollback handling when an operation fails.
- Use of `SELECT ... FOR UPDATE` to lock an account row during transaction processing.

## 6. Advanced DBMS Features

### SQL Business Queries
The `database/queries.sql` file contains 14 business-oriented queries covering:
- Retrieving customer and account information.
- Joining related tables.
- Identifying customers without accounts.
- Summarizing accounts and balances.
- Grouping and aggregating transaction data.
- Branch-wise account summaries.
- Filtering grouped results using `HAVING`.
- Finding accounts without transaction records.
- Monthly transaction summaries.

### Views
Three views have been defined:
- `vw_customer_accounts`
- `vw_branch_summary`
- `vw_transaction_details`

These views simplify repeated queries by presenting related data from multiple tables.

### Stored Function
- `fn_account_balance(p_account_id)` returns the balance associated with an account ID.

### Stored Procedures
- `sp_get_account_details(p_account_id)` retrieves account details together with the associated branch name.
- `sp_transaction_summary()` summarizes successful transactions by transaction type.

### Trigger
- `trg_validate_transaction_amount` runs before a transaction record is inserted and rejects amounts less than or equal to zero.

The advanced SQL definitions have been prepared and reviewed. Final verification of their presence, execution, and outputs should be completed before submission.

## 7. Testing Performed

The following workflows have been tested during development:
- Python-to-MySQL connectivity.
- Customer registration and listing.
- Account creation and account listing.
- Account detail and transaction-history pages.
- Deposit and withdrawal workflows.
- Balance updates following transactions.
- Rejection of an excessive withdrawal.
- Validation of nonpositive transaction amounts.
- Execution and inspection of advanced SQL features during development.

Earlier transaction tests included a deposit of ₹80,000 and a withdrawal of ₹5,000, producing an expected balance of ₹75,000 at that stage. Later testing modified account data, so this historical balance should not be treated as the current database state.

A final regression test and review of the current database contents remain necessary.

## 8. Remaining Finalization Tasks

- Verify that all six tables and the expected database objects exist.
- Re-run selected SQL queries, views, functions, procedures, and trigger tests against the current database.
- Test referential integrity and relevant constraints.
- Perform a final application workflow test.
- Review validation and error handling.
- Review schema consistency and normalization.
- Finalize the README with setup and execution instructions.
- Capture application and database screenshots.
- Complete the project report and ER diagram review.
- Verify that GitHub contains the final source code and documentation.
- Prepare to explain the schema, SQL features, application workflow, and testing results during the viva.

## 9. Current Status

**Core application:** Implemented; principal workflows have been tested.

**Advanced SQL:** Definitions prepared and reviewed; final verification remains.

**Documentation and submission:** Final update, screenshots, report, and repository review remain.

**Project scope:** The optional loan module is excluded.

**Next milestone:** Verify the final database state, complete regression testing, update project documentation, and prepare for the viva.
