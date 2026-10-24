
USE project_kashi;

-- 1. Display all registered customers
SELECT *
FROM CUSTOMER
ORDER BY CustomerID;

-- 2. Customer account report
SELECT
    c.CustomerID,
    c.FirstName,
    c.LastName,
    a.AccountNumber,
    a.AccountType,
    a.Balance,
    a.Status,
    ah.HolderType
FROM CUSTOMER c
JOIN ACCOUNT_HOLDER ah ON c.CustomerID = ah.CustomerID
JOIN ACCOUNT a ON ah.AccountID = a.AccountID
ORDER BY c.CustomerID;

-- 3. List accounts with their branch details
SELECT
    a.AccountNumber,
    a.AccountType,
    a.Balance,
    a.Status,
    b.BranchName,
    b.City AS BranchCity
FROM ACCOUNT a
JOIN BRANCH b ON a.BranchID = b.BranchID;

-- 4. Find customers who do not own an account
SELECT
    c.CustomerID,
    c.FirstName,
    c.LastName
FROM CUSTOMER c
LEFT JOIN ACCOUNT_HOLDER ah ON c.CustomerID = ah.CustomerID
WHERE ah.AccountID IS NULL;

-- 5. Display transaction history with account numbers
SELECT
    t.TransactionID,
    a.AccountNumber,
    t.TransactionType,
    t.Amount,
    t.TransactionDate,
    t.TransactionStatus,
    t.Description
FROM BANK_TRANSACTION t
JOIN ACCOUNT a ON t.AccountID = a.AccountID
ORDER BY t.TransactionDate DESC;

-- 6. Account count and total balance by account type
SELECT
    AccountType,
    COUNT(*) AS NumberOfAccounts,
    SUM(Balance) AS TotalBalance,
    AVG(Balance) AS AverageBalance
FROM ACCOUNT
GROUP BY AccountType;

-- 7. Total successful transaction amount by transaction type
SELECT
    TransactionType,
    COUNT(*) AS TransactionCount,
    SUM(Amount) AS TotalAmount
FROM BANK_TRANSACTION
WHERE TransactionStatus = 'Success'
GROUP BY TransactionType;

-- 8. Branch-wise account summary
SELECT
    b.BranchID,
    b.BranchName,
    COUNT(a.AccountID) AS NumberOfAccounts,
    COALESCE(SUM(a.Balance), 0) AS TotalBalance
FROM BRANCH b
LEFT JOIN ACCOUNT a ON b.BranchID = a.BranchID
GROUP BY b.BranchID, b.BranchName;

-- 9. Customers with more than one account
SELECT
    c.CustomerID,
    c.FirstName,
    c.LastName,
    COUNT(ah.AccountID) AS NumberOfAccounts
FROM CUSTOMER c
JOIN ACCOUNT_HOLDER ah ON c.CustomerID = ah.CustomerID
GROUP BY c.CustomerID, c.FirstName, c.LastName
HAVING COUNT(ah.AccountID) > 1;

-- 10. Accounts with a balance greater than ₹10,000
SELECT
    AccountNumber,
    AccountType,
    Balance
FROM ACCOUNT
WHERE Balance > 10000
ORDER BY Balance DESC;

-- 11. Customers and their total account balances
SELECT
    c.CustomerID,
    c.FirstName,
    c.LastName,
    SUM(a.Balance) AS TotalBalance
FROM CUSTOMER c
JOIN ACCOUNT_HOLDER ah ON c.CustomerID = ah.CustomerID
JOIN ACCOUNT a ON ah.AccountID = a.AccountID
GROUP BY c.CustomerID, c.FirstName, c.LastName
ORDER BY TotalBalance DESC;

-- 12. Employee details with their branch names
SELECT
    e.EmployeeID,
    e.EmployeeName,
    e.Designation,
    e.Salary,
    b.BranchName
FROM EMPLOYEE e
JOIN BRANCH b ON e.BranchID = b.BranchID;

-- 13. Monthly transaction summary
SELECT
    YEAR(TransactionDate) AS TransactionYear,
    MONTH(TransactionDate) AS TransactionMonth,
    COUNT(*) AS TransactionCount,
    SUM(Amount) AS TotalAmount
FROM BANK_TRANSACTION
WHERE TransactionStatus = 'Success'
GROUP BY YEAR(TransactionDate), MONTH(TransactionDate)
ORDER BY TransactionYear DESC, TransactionMonth DESC;

-- 14. Accounts with no recorded transactions
SELECT
    a.AccountID,
    a.AccountNumber,
    a.AccountType,
    a.Balance
FROM ACCOUNT a
LEFT JOIN BANK_TRANSACTION t ON a.AccountID = t.AccountID
WHERE t.TransactionID IS NULL;
