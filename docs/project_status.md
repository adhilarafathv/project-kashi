# Project KASHI — Project Status

**Last Updated:** October 18, 2026

## 1. Project Overview

Project KASHI is an educational Banking Management System developed to demonstrate database design, SQL operations, relational integrity, and communication between a frontend, backend, and database.

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
│   └── queries.sql
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

The six implemented core tables are:

1. `CUSTOMER` — stores customer information.
2. `BRANCH` — stores bank branch information.
3. `EMPLOYEE` — stores employee information and branch assignments.
4. `ACCOUNT` — stores account numbers, account types, balances, status, and branch assignments.
5. `ACCOUNT_HOLDER` — connects customers and accounts.
6. `BANK_TRANSACTION` — stores deposit and withdrawal records.

### Keys and Constraints

- Primary keys uniquely identify records.
- Foreign keys maintain relationships between tables.
- Unique constraints prevent duplicate values in designated columns, including customer mobile numbers and account numbers.
- `ACCOUNT_HOLDER` uses a composite primary key consisting of `CustomerID` and `AccountID`.
- Required columns use `NOT NULL` constraints.
- Monetary values use `DECIMAL` data types.

The database schema and ER design are documented in `database/schema.sql` and `docs/er_diagram.md`, respectively.

## 4. Database Relationships and Cardinalities

### 4.1 CUSTOMER to ACCOUNT — M:N

One customer may hold several accounts, and one account may be shared by several customers.

**Implementation:** `ACCOUNT_HOLDER` connects `CustomerID` and `AccountID`. It also stores `HolderSince` and `HolderType`.

### 4.2 BRANCH to EMPLOYEE — 1:N

One branch can employ many employees. Each employee is assigned to one branch.

**Implementation:** `EMPLOYEE.BranchID` references `BRANCH.BranchID`.

### 4.3 BRANCH to ACCOUNT — 1:N

One branch can manage many accounts. Each account belongs to one branch in this design.

**Implementation:** `ACCOUNT.BranchID` references `BRANCH.BranchID`.

### 4.4 CUSTOMER to LOAN — 1:N (Optional)

A customer can have multiple loans. Each loan record identifies one customer.

**Planned implementation:** `LOAN.CustomerID` references `CUSTOMER.CustomerID`.

The loan module is excluded from the current implementation.

### 4.5 LOAN to LOAN_PAYMENT — 1:N (Optional)

One loan can have many repayments, while each payment belongs to one loan.

**Planned implementation:** `LOAN_PAYMENT.LoanID` references `LOAN.LoanID`.

The loan and loan-payment tables have not been implemented because the optional loan module was skipped.

### 4.6 ACCOUNT to BANK_TRANSACTION — 1:N

One account can have many transaction records. Each transaction record refers to one account.

**Implementation:** `BANK_TRANSACTION.AccountID` references `ACCOUNT.AccountID`.

The physical table is named `BANK_TRANSACTION` instead of `TRANSACTION`.

## 5. Completed Features — Batch 1

- Established a Python-to-MySQL database connection.
- Configured the Flask application and template/static directories.
- Implemented customer registration.
- Implemented customer listing.
- Implemented account creation.
- Linked accounts to customers and branches.
- Implemented account listing.
- Used parameterized SQL queries for database operations.
- Added basic error handling and database resource cleanup.

## 6. Completed Features — Batch 2

### Account Management

- Displayed account details.
- Displayed account numbers, owners, account types, branches, balances, and statuses.
- Linked account listings to individual account detail pages.

### Banking Transactions

- Implemented deposits.
- Implemented withdrawals.
- Recorded transaction amounts, types, descriptions, reference numbers, timestamps, and statuses.
- Displayed transaction history for individual accounts.

### Validation and Transaction Safety

- Validated transaction types and monetary amounts.
- Rejected nonpositive amounts.
- Prevented withdrawals exceeding the available balance.
- Restricted transactions to accounts with `Active` status.
- Used database transactions to group balance updates and transaction-record inserts.
- Added rollback handling for failed operations.
- Used `SELECT ... FOR UPDATE` to lock account rows during transaction processing.

## 7. Testing Performed

- Verified the Python-to-MySQL database connection.
- Registered customers.
- Created accounts, including a Salary account.
- Deposited ₹80,000 into a test account.
- Withdrew ₹5,000 and verified the expected balance of ₹75,000.
- Attempted an excessive withdrawal and verified that it was rejected without changing the balance.
- Verified the account transaction workflow through the web application.

These tests confirm the basic workflows tested so far. Broader testing is still required.

## 8. Pending Work — Batch 3: Advanced DBMS Requirements

- Prepare at least 10 meaningful SQL business queries.
- Demonstrate joins and aggregate queries.
- Create and demonstrate database views.
- Implement and test stored functions.
- Implement and test stored procedures.
- Implement and test triggers.
- Demonstrate transaction handling and rollback.
- Test referential integrity and other database constraints.

## 9. Pending Work — Batch 4: Finalization

- Improve the frontend styling and responsive layout.
- Improve user-facing validation and error messages.
- Review database normalization and schema consistency.
- Perform broader application and database testing.
- Verify that `schema.sql` and `queries.sql` contain the intended SQL.
- Update the README with setup and execution instructions.
- Capture screenshots of the application and database results.
- Complete the project report.
- Verify GitHub contains the final source code and documentation.

## 10. Current Status

**Batches 1 and 2:** Core database connectivity, customer management, account management, and tested deposit/withdrawal workflows are implemented.

**Current milestone:** Complete Batch 3 — advanced SQL and DBMS requirements.

**Project scope note:** The optional loan module is excluded from the current implementation.