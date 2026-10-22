"""Revenue per customer per month from an orders CSV.

Usage:
    python revenue_report.py [path/to/orders.csv]

Expected columns: order_id, customer_id, amount, created_at
Invalid rows are skipped and reported to stderr.
"""

import csv
import sys
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation

REQUIRED_COLUMNS = ["order_id", "customer_id", "amount", "created_at"]
DATE_FORMATS = ["%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]


def parse_date(value):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"invalid created_at '{value}'")


def validate_row(row, seen_ids):
    """Return (customer_id, month, amount) or raise ValueError with a reason."""
    order_id = (row.get("order_id") or "").strip()
    customer_id = (row.get("customer_id") or "").strip()
    amount_raw = (row.get("amount") or "").strip()
    created_raw = (row.get("created_at") or "").strip()

    if not order_id:
        raise ValueError("missing order_id")
    if order_id in seen_ids:
        raise ValueError(f"duplicate order_id '{order_id}'")
    if not customer_id:
        raise ValueError("missing customer_id")

    try:
        amount = Decimal(amount_raw)
    except InvalidOperation:
        raise ValueError(f"invalid amount '{amount_raw}'")
    if not amount.is_finite() or amount <= 0:
        raise ValueError(f"amount must be a positive number, got '{amount_raw}'")

    if not created_raw:
        raise ValueError("missing created_at")
    month = parse_date(created_raw).strftime("%Y-%m")

    seen_ids.add(order_id)
    return customer_id, month, amount


def build_report(path):
    revenue = defaultdict(Decimal)
    invalid = []
    seen_ids = set()

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"Error: missing columns in header: {', '.join(missing)}")

        # line 1 is the header, so data starts at line 2
        for line_no, row in enumerate(reader, start=2):
            if None in row:
                invalid.append((line_no, "too many columns"))
                continue
            try:
                customer_id, month, amount = validate_row(row, seen_ids)
            except ValueError as e:
                invalid.append((line_no, str(e)))
                continue
            revenue[(customer_id, month)] += amount

    return revenue, invalid


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "orders.csv"
    try:
        revenue, invalid = build_report(path)
    except FileNotFoundError:
        raise SystemExit(f"Error: file not found: {path}")

    if invalid:
        print(f"Skipped {len(invalid)} invalid row(s):", file=sys.stderr)
        for line_no, reason in invalid:
            print(f"  line {line_no}: {reason}", file=sys.stderr)
        print(file=sys.stderr)

    # highest revenue first; ties broken by customer, then month
    rows = sorted(revenue.items(), key=lambda kv: (-kv[1], kv[0][0], kv[0][1]))

    print(f"{'customer_id':<12} {'month':<8} {'revenue':>12}")
    print("-" * 34)
    for (customer_id, month), total in rows:
        print(f"{customer_id:<12} {month:<8} {total:>12.2f}")


if __name__ == "__main__":
    main()
