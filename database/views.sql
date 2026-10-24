
USE project_kashi;

-- View 1: Customer account details
CREATE OR REPLACE VIEW vw_customer_accounts AS
SELECT
    c.CustomerID,
    c.FirstName,
    c.LastName,
    a.AccountID,
    a.AccountNumber,
    a.AccountType,
    a.Balance,
    a.Status,
    ah.HolderType,
    b.BranchName
FROM CUSTOMER c
JOIN ACCOUNT_HOLDER ah
    ON c.CustomerID = ah.CustomerID
JOIN ACCOUNT a
    ON ah.AccountID = a.AccountID
JOIN BRANCH b
    ON a.BranchID = b.BranchID;

-- View 2: Branch account summary
CREATE OR REPLACE VIEW vw_branch_summary AS
SELECT
    b.BranchID,
    b.BranchName,
    b.City,
    COUNT(a.AccountID) AS TotalAccounts,
    COALESCE(SUM(a.Balance), 0) AS TotalBalance
FROM BRANCH b
LEFT JOIN ACCOUNT a
    ON b.BranchID = a.BranchID
GROUP BY b.BranchID, b.BranchName, b.City;

-- View 3: Transaction details
CREATE OR REPLACE VIEW vw_transaction_details AS
SELECT
    t.TransactionID,
    a.AccountNumber,
    a.AccountType,
    t.TransactionType,
    t.Amount,
    t.TransactionDate,
    t.TransactionStatus,
    t.Description,
    t.ReferenceNumber
FROM BANK_TRANSACTION t
JOIN ACCOUNT a
    ON t.AccountID = a.AccountID;
