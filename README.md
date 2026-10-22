# Orders Revenue Report

Reads `orders.csv` (`order_id, customer_id, amount, created_at`), skips invalid rows
(reported to stderr with line number and reason), and prints revenue per customer
per month, sorted by revenue (highest first).

Standard library only, Python 3.8+.

## Usage

```bash
python revenue_report.py              # reads ./orders.csv
python revenue_report.py path/to/file.csv
```

## Invalid rows

A row is skipped when:

- `order_id` or `customer_id` is missing, or `order_id` is duplicated
- `amount` is not a number, or is zero/negative
- `created_at` is missing or not an ISO date (`2024-01-05`, `2024-01-05 14:30:00`)

## Example output

Using the sample `orders.csv`:

```
Skipped 6 invalid row(s):
  line 12: invalid amount
  line 13: missing order_id or customer_id
  line 14: non-positive amount '-40.00'
  line 15: month must be in 1..12, not 13
  line 16: duplicate order_id '3'
  line 17: Invalid isoformat string: ''

customer_id  month       revenue
C004         2024-02      500.00
C003         2024-01      300.00
C001         2024-03      210.00
C001         2024-01      165.75
C002         2024-02      150.00
C004         2024-03      120.00
C001         2024-02       99.99
C002         2024-01       80.00
C002         2024-03       60.00
C003         2024-02       20.00
```
