# Week 3 - Superstore Query Results

Output of every query in `analysis.sql`, run against `superstore.db`. Large result sets are previewed to a few rows; the full count is noted under each.

## Step 1 - Table row counts

_3 row(s)._

| table_name | rows |
| --- | --- |
| customers | 793 |
| orders | 9994 |
| products | 1862 |

---

## Q1 - Orders with sales above the average (Subquery)

_Showing 10 of 2360 rows._

| row_id | order_id | customer_id | sales |
| --- | --- | --- | --- |
| 2698 | CA-2014-145317 | SM-20320 | 22638.48 |
| 6827 | CA-2016-118689 | TC-20980 | 17499.95 |
| 8154 | CA-2017-140151 | RB-19360 | 13999.96 |
| 2624 | CA-2017-127180 | TA-21385 | 11199.97 |
| 4191 | CA-2017-166709 | HL-15040 | 10499.97 |
| 9040 | CA-2016-117121 | AB-10105 | 9892.74 |
| 4099 | CA-2014-116904 | SC-20095 | 9449.95 |
| 4278 | US-2016-107440 | BS-11365 | 9099.93 |
| 8489 | CA-2016-158841 | SE-20110 | 8749.95 |
| 6426 | CA-2016-143714 | CC-12370 | 8399.98 |

---

## Q2 - Highest sales order per customer (Subquery)

_Showing 10 of 795 rows._

| customer_id | order_id | sales |
| --- | --- | --- |
| SM-20320 | CA-2014-145317 | 22638.48 |
| TC-20980 | CA-2016-118689 | 17499.95 |
| RB-19360 | CA-2017-140151 | 13999.96 |
| TA-21385 | CA-2017-127180 | 11199.97 |
| HL-15040 | CA-2017-166709 | 10499.97 |
| AB-10105 | CA-2016-117121 | 9892.74 |
| SC-20095 | CA-2014-116904 | 9449.95 |
| BS-11365 | US-2016-107440 | 9099.93 |
| SE-20110 | CA-2016-158841 | 8749.95 |
| CC-12370 | CA-2016-143714 | 8399.98 |

---

## Q3 - Total sales per customer (CTE)

_Showing 10 of 793 rows._

| customer_name | total_sales |
| --- | --- |
| Sean Miller | 25043.05 |
| Tamara Chand | 19052.22 |
| Raymond Buch | 15117.34 |
| Tom Ashbrook | 14595.62 |
| Adrian Barton | 14473.57 |
| Ken Lonsdale | 14175.23 |
| Sanjit Chand | 14142.33 |
| Hunter Lopez | 12873.3 |
| Sanjit Engle | 12209.44 |
| Christopher Conant | 12129.07 |

---

## Q4 - Customers above average total sales (CTE + Subquery)

_Showing 10 of 294 rows._

| customer_name | total_sales |
| --- | --- |
| Sean Miller | 25043.05 |
| Tamara Chand | 19052.22 |
| Raymond Buch | 15117.34 |
| Tom Ashbrook | 14595.62 |
| Adrian Barton | 14473.57 |
| Ken Lonsdale | 14175.23 |
| Sanjit Chand | 14142.33 |
| Hunter Lopez | 12873.3 |
| Sanjit Engle | 12209.44 |
| Christopher Conant | 12129.07 |

---

## Q5 - Rank all customers by total sales (Window Function)

_Showing 10 of 793 rows._

| customer_name | total_sales | sales_rank |
| --- | --- | --- |
| Sean Miller | 25043.05 | 1 |
| Tamara Chand | 19052.22 | 2 |
| Raymond Buch | 15117.34 | 3 |
| Tom Ashbrook | 14595.62 | 4 |
| Adrian Barton | 14473.57 | 5 |
| Ken Lonsdale | 14175.23 | 6 |
| Sanjit Chand | 14142.33 | 7 |
| Hunter Lopez | 12873.3 | 8 |
| Sanjit Engle | 12209.44 | 9 |
| Christopher Conant | 12129.07 | 10 |

---

## Q6 - Order sequence within each customer (Window + PARTITION BY)

_Showing 12 of 9994 rows._

| customer_id | order_id | order_date | sales | order_seq |
| --- | --- | --- | --- | --- |
| AA-10315 | CA-2014-128055 | 2014-03-31 | 673.57 | 1 |
| AA-10315 | CA-2014-128055 | 2014-03-31 | 52.98 | 2 |
| AA-10315 | CA-2014-138100 | 2014-09-15 | 14.94 | 3 |
| AA-10315 | CA-2014-138100 | 2014-09-15 | 14.56 | 4 |
| AA-10315 | CA-2015-121391 | 2015-10-04 | 26.96 | 5 |
| AA-10315 | CA-2016-103982 | 2016-03-03 | 3930.07 | 6 |
| AA-10315 | CA-2016-103982 | 2016-03-03 | 2.3 | 7 |
| AA-10315 | CA-2016-103982 | 2016-03-03 | 431.98 | 8 |
| AA-10315 | CA-2016-103982 | 2016-03-03 | 41.72 | 9 |
| AA-10315 | CA-2017-147039 | 2017-06-29 | 362.94 | 10 |
| AA-10315 | CA-2017-147039 | 2017-06-29 | 11.54 | 11 |
| AA-10375 | CA-2014-158064 | 2014-04-21 | 16.52 | 1 |

---

## Q7 - Top 3 customers by total sales (Window Function)

_3 row(s)._

| customer_name | total_sales | sales_rank |
| --- | --- | --- |
| Sean Miller | 25043.05 | 1 |
| Tamara Chand | 19052.22 | 2 |
| Raymond Buch | 15117.34 | 3 |

---

## Step 3 - Final combined: Customer, Total Sales, Rank (JOIN + CTE + Window)

_Showing 10 of 793 rows._

| customer_name | total_sales | sales_rank |
| --- | --- | --- |
| Sean Miller | 25043.05 | 1 |
| Tamara Chand | 19052.22 | 2 |
| Raymond Buch | 15117.34 | 3 |
| Tom Ashbrook | 14595.62 | 4 |
| Adrian Barton | 14473.57 | 5 |
| Ken Lonsdale | 14175.23 | 6 |
| Sanjit Chand | 14142.33 | 7 |
| Hunter Lopez | 12873.3 | 8 |
| Sanjit Engle | 12209.44 | 9 |
| Christopher Conant | 12129.07 | 10 |

---

## Mini Project Q1 - Top 5 customers

_5 row(s)._

| customer_name | total_sales |
| --- | --- |
| Sean Miller | 25043.05 |
| Tamara Chand | 19052.22 |
| Raymond Buch | 15117.34 |
| Tom Ashbrook | 14595.62 |
| Adrian Barton | 14473.57 |

---

## Mini Project Q2 - Bottom 5 customers

_5 row(s)._

| customer_name | total_sales |
| --- | --- |
| Thais Sissman | 4.83 |
| Lela Donovan | 5.3 |
| Carl Jackson | 16.52 |
| Mitch Gastineau | 16.74 |
| Roy Skaria | 22.33 |

---

## Mini Project Q3 - Customers with only one order

_Showing 10 of 12 rows._

| customer_name | order_count |
| --- | --- |
| Anemone Ratner | 1 |
| Anthony O'Donnell | 1 |
| Carl Jackson | 1 |
| Jenna Caffey | 1 |
| Jocasta Rupert | 1 |
| Lela Donovan | 1 |
| Mitch Gastineau | 1 |
| Patricia Hirasaki | 1 |
| Ricardo Emerson | 1 |
| Roland Murray | 1 |

---

## Mini Project Q4 - Customers with above-average sales

_Showing 10 of 294 rows._

| customer_name | total_sales |
| --- | --- |
| Sean Miller | 25043.05 |
| Tamara Chand | 19052.22 |
| Raymond Buch | 15117.34 |
| Tom Ashbrook | 14595.62 |
| Adrian Barton | 14473.57 |
| Ken Lonsdale | 14175.23 |
| Sanjit Chand | 14142.33 |
| Hunter Lopez | 12873.3 |
| Sanjit Engle | 12209.44 |
| Christopher Conant | 12129.07 |

---

## Mini Project Q5 - Highest order value per customer

_Showing 10 of 793 rows._

| customer_name | highest_order_value |
| --- | --- |
| Sean Miller | 22638.48 |
| Tamara Chand | 17499.95 |
| Raymond Buch | 13999.96 |
| Tom Ashbrook | 11199.97 |
| Hunter Lopez | 10499.97 |
| Adrian Barton | 9892.74 |
| Sanjit Chand | 9449.95 |
| Bill Shonely | 9099.93 |
| Sanjit Engle | 8749.95 |
| Christopher Conant | 8399.98 |

---

