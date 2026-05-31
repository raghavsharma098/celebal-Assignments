SELECT product_name,
       unit_price,
       CASE
           WHEN unit_price < 1000               THEN 'Budget'
           WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
           ELSE 'Premium'
       END AS price_tier
FROM   products
ORDER BY unit_price;

SELECT
    COUNT(CASE WHEN status = 'Delivered'  THEN 1 END) AS delivered_count,
    COUNT(CASE WHEN status <> 'Delivered' THEN 1 END) AS not_delivered_count
FROM orders;

-- Q26. ACID:
-- Atomicity - a transaction is all-or-nothing. In a bank transfer, if the debit
--   succeeds but the credit fails, the whole transaction rolls back so money is
--   never lost.
-- Consistency - a transaction moves the database from one valid state to another,
--   respecting every constraint. A transfer that would make a balance negative
--   is rejected.
-- Isolation - concurrent transactions don't see each other's partial work. Two
--   people buying the last unit in stock can't both succeed and oversell it.
-- Durability - once committed, changes survive a crash. An order placed just
--   before the server dies is still there after restart.

-- Q27. New order + items + stock update, atomically. The handler rolls
-- everything back if any statement fails.
DELIMITER $$

CREATE PROCEDURE sp_place_order_1011()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'Transaction rolled back due to an error.' AS result;
    END;

    START TRANSACTION;

    INSERT INTO orders (order_id, customer_id, order_date, status, total_amount)
    VALUES (1011, 102, CURDATE(), 'Pending', 1598.00);

    INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price, discount_pct)
    VALUES (5016, 1011, 206, 1, 1299.00, 0);

    INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price, discount_pct)
    VALUES (5017, 1011, 208, 1, 599.00, 0);

    UPDATE products SET stock_qty = stock_qty - 1 WHERE product_id = 206;
    UPDATE products SET stock_qty = stock_qty - 1 WHERE product_id = 208;

    COMMIT;
    SELECT 'Order 1011 placed successfully.' AS result;
END$$

DELIMITER ;

CALL sp_place_order_1011();

SELECT * FROM orders      WHERE order_id = 1011;
SELECT * FROM order_items WHERE order_id = 1011;
SELECT product_id, product_name, stock_qty FROM products WHERE product_id IN (206, 208);
