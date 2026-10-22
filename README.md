# Orders Revenue Report

A Python script that reads `orders.csv`, skips and reports invalid rows, and prints
revenue per customer per month, sorted by revenue (highest first).

No external dependencies — only the Python standard library (Python 3.8+).

## Input format

`orders.csv` must have a header with these columns:

| column        | description                                                        |
|---------------|--------------------------------------------------------------------|
| `order_id`    | unique order identifier                                            |
| `customer_id` | customer identifier                                                |
| `amount`      | positive number, e.g. `120.50`                                     |
| `created_at`  | `YYYY-MM-DD`, `YYYY-MM-DD HH:MM:SS` or `YYYY-MM-DDTHH:MM:SS`       |

## Usage

```bash
python revenue_report.py              # reads ./orders.csv
python revenue_report.py path/to/file.csv
```

## Validation rules

A row is skipped (and reported to stderr with its line number and reason) when:

- `order_id` is missing or duplicated
- `customer_id` is missing
- `amount` is not a number, or is zero/negative
- `created_at` is missing or not a valid date
- the row has more columns than the header

Amounts are summed with `Decimal` to avoid floating-point rounding errors.

## Example output

Using the sample `orders.csv` in this repo:

```
Skipped 6 invalid row(s):
  line 12: invalid amount 'abc'
  line 13: missing customer_id
  line 14: amount must be a positive number, got '-40.00'
  line 15: invalid created_at '2024-13-01'
  line 16: duplicate order_id '3'
  line 17: missing created_at

customer_id  month         revenue
----------------------------------
C004         2024-02        500.00
C003         2024-01        300.00
C001         2024-03        210.00
C001         2024-01        165.75
C002         2024-02        150.00
C004         2024-03        120.00
C001         2024-02         99.99
C002         2024-01         80.00
C002         2024-03         60.00
C003         2024-02         20.00
```
