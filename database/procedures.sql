
USE project_kashi;

DROP PROCEDURE IF EXISTS sp_get_account_details;
DROP PROCEDURE IF EXISTS sp_transaction_summary;

DELIMITER //

CREATE PROCEDURE sp_get_account_details(IN p_account_id INT)
BEGIN
    SELECT
        a.AccountID,
        a.AccountNumber,
        a.AccountType,
        a.Balance,
        a.Status,
        b.BranchName
    FROM ACCOUNT a
    JOIN BRANCH b
        ON a.BranchID = b.BranchID
    WHERE a.AccountID = p_account_id;
END //

CREATE PROCEDURE sp_transaction_summary()
BEGIN
    SELECT
        TransactionType,
        COUNT(*) AS TransactionCount,
        SUM(Amount) AS TotalAmount
    FROM BANK_TRANSACTION
    WHERE TransactionStatus = 'Success'
    GROUP BY TransactionType;
END //

DELIMITER ;
