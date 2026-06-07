# Week 3 - Customer Sales Insights

Analysis of the Superstore dataset using subqueries, CTEs and window functions.
Everything here is reproduced by running `load_data.py` and then `run_queries.py`;
the raw output sits in [query_results.md](query_results.md) and the SQL itself in
[analysis.sql](analysis.sql).

## How the data is set up

The full CSV (9,994 line items) is imported into `superstore_raw`. From that single
table three smaller ones are carved out with `SELECT DISTINCT`:

| Table | Rows | What it holds |
| --- | --- | --- |
| customers | 793 | one row per customer (id, name, segment) |
| orders | 9,994 | one row per order line (sales, quantity, profit, dates) |
| products | 1,862 | one row per product (category, sub-category, name) |

Across all orders the store booked **$2,297,200.86** in sales, the average order line
is **$229.86**, and the average customer is worth **$2,896.85** in lifetime sales.

## What the numbers say

**A small group of customers carries the revenue.** Only **294 of 793 customers (37%)**
spend above the average, yet they account for the large majority of sales. Ranking by
total spend, the top three are **Sean Miller ($25,043), Tamara Chand ($19,052) and
Raymond Buch ($15,117)** — Sean Miller alone is worth more than the bottom hundreds of
customers combined.

**Big totals come from big single orders, not steady spending.** Each of the top
customers has one standout order that drives most of their total: Sean Miller's best
order is **$22,638** out of his $25,043 lifetime, and Tamara Chand's best is **$17,499**
out of $19,052. The "highest order value per customer" list mirrors the "top customers"
list almost exactly, which tells us these are occasional large-ticket buyers rather than
frequent shoppers.

**The long tail is thin.** The bottom five customers — Thais Sissman ($4.83),
Lela Donovan ($5.30), Carl Jackson ($16.52), Mitch Gastineau ($16.74) and
Roy Skaria ($22.33) — barely register, and **12 customers placed only a single order**.
These are the obvious targets for re-engagement campaigns.

**Most order lines are small.** Only **2,360 of 9,994 lines (24%)** beat the average
sale value, confirming that a few large transactions pull the average well above the
typical order.

## Business questions (mini project)

| # | Question | Answer |
| --- | --- | --- |
| 1 | Top 5 customers | Sean Miller, Tamara Chand, Raymond Buch, Tom Ashbrook, Adrian Barton |
| 2 | Bottom 5 customers | Thais Sissman, Lela Donovan, Carl Jackson, Mitch Gastineau, Roy Skaria |
| 3 | Customers with only one order | 12 customers (e.g. Anemone Ratner, Carl Jackson, Lela Donovan) |
| 4 | Above-average customers | 294 customers spend more than the $2,896.85 average |
| 5 | Highest order value per customer | Sean Miller tops it at $22,638.48 |

## Takeaways

- Revenue is concentrated: protect and grow the ~290 above-average customers, because
  losing one of the top names hurts disproportionately.
- The top spenders look like project / bulk buyers driven by single large orders —
  worth a dedicated account-management touch to turn one big order into repeat business.
- A visible long tail of one-order and very-low-value customers is the clearest
  opportunity for win-back and upsell activity.
