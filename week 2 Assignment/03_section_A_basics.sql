-- Section A - SQL Basics

-- Q1. All columns and rows from customers
SELECT *
FROM customers;

-- Q2. Only first_name, last_name and city
SELECT first_name, last_name, city
FROM customers;

-- Q3. Unique product categories
SELECT DISTINCT category
FROM products;

-- Q4. Primary keys of each table
-- customers -> customer_id, products -> product_id,
-- orders -> order_id, order_items -> item_id.
-- A primary key must be unique and not null because it is the single value
-- used to identify a row. If it repeated, joins could not tell rows apart;
-- if it were null the row would have no identity and could not be referenced
-- by a foreign key.

-- Q5. Constraints on customers.email
-- The email column is UNIQUE and NOT NULL. Inserting a duplicate email is
-- rejected with a unique-constraint error (e.g. ERROR 1062 in MySQL) and the
-- table is left unchanged.
-- Example that would fail on the loaded data:
-- INSERT INTO customers VALUES
--   (109, 'Test', 'User', 'aarav.s@email.com', 'Mumbai', 'Maharashtra', '2024-09-01', FALSE);

-- Q6. Inserting a product with unit_price = -50
-- This violates CHECK (unit_price > 0), so the row is rejected and nothing is
-- inserted.
-- INSERT INTO products VALUES
--   (209, 'Test Product', 'Electronics', 'TestBrand', -50.00, 100);
