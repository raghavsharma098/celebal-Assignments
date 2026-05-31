SELECT *
FROM customers;

SELECT first_name, last_name, city
FROM customers;

SELECT DISTINCT category
FROM products;

-- Q4. Primary keys: customers.customer_id, products.product_id,
-- orders.order_id, order_items.item_id. A primary key must be unique and not
-- null because it is the single value that identifies a row. Duplicate keys
-- would make rows indistinguishable and break joins; a null key would leave a
-- row with no identity that foreign keys could reference.

-- Q5. customers.email is UNIQUE and NOT NULL. Inserting a duplicate email
-- raises a unique-constraint error (MySQL ERROR 1062); the row is rejected and
-- the table is left unchanged. For example, this fails on the loaded data:
--   INSERT INTO customers VALUES
--   (109,'Test','User','aarav.s@email.com','Mumbai','Maharashtra','2024-09-01',FALSE);

-- Q6. Inserting a product with unit_price = -50 violates CHECK (unit_price > 0),
-- so the database rejects the row and nothing is inserted. For example:
--   INSERT INTO products VALUES
--   (209,'Test Product','Electronics','TestBrand',-50.00,100);
