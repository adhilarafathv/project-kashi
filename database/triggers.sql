USE project_kashi;

DROP TRIGGER IF EXISTS trg_validate_transaction_amount;

DELIMITER $$

CREATE TRIGGER trg_validate_transaction_amount
BEFORE INSERT ON BANK_TRANSACTION
FOR EACH ROW
BEGIN
    IF NEW.Amount <= 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Transaction amount must be positive';
    END IF;
END $$

DELIMITER ;