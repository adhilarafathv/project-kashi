
USE project_kashi;

DROP FUNCTION IF EXISTS fn_account_balance;

DELIMITER //

CREATE FUNCTION fn_account_balance(p_account_id INT)
RETURNS DECIMAL(15,2)
READS SQL DATA
BEGIN
    DECLARE v_balance DECIMAL(15,2);

    SELECT Balance
    INTO v_balance
    FROM ACCOUNT
    WHERE AccountID = p_account_id;

    RETURN v_balance;
END //

DELIMITER ;
