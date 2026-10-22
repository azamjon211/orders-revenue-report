"""Revenue per customer per month from orders.csv.

Usage: python revenue_report.py [path/to/orders.csv]
"""

import csv
import sys
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "orders.csv"
    revenue = defaultdict(Decimal)
    seen_ids = set()
    invalid = []

    with open(path, newline="", encoding="utf-8") as f:
        # line 1 is the header, so data starts at line 2
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            order_id = (row.get("order_id") or "").strip()
            customer_id = (row.get("customer_id") or "").strip()
            try:
                if not order_id or not customer_id:
                    raise ValueError("missing order_id or customer_id")
                if order_id in seen_ids:
                    raise ValueError(f"duplicate order_id '{order_id}'")
                amount = Decimal(row.get("amount") or "")
                if amount <= 0:
                    raise ValueError(f"non-positive amount '{amount}'")
                month = datetime.fromisoformat((row.get("created_at") or "").strip()).strftime("%Y-%m")
            except (ValueError, InvalidOperation) as e:
                reason = "invalid amount" if isinstance(e, InvalidOperation) else str(e)
                invalid.append((line_no, reason))
                continue
            seen_ids.add(order_id)
            revenue[(customer_id, month)] += amount

    if invalid:
        print(f"Skipped {len(invalid)} invalid row(s):", file=sys.stderr)
        for line_no, reason in invalid:
            print(f"  line {line_no}: {reason}", file=sys.stderr)
        print(file=sys.stderr)

    print(f"{'customer_id':<12} {'month':<8} {'revenue':>10}")
    for (customer_id, month), total in sorted(revenue.items(), key=lambda kv: -kv[1]):
        print(f"{customer_id:<12} {month:<8} {total:>10.2f}")


if __name__ == "__main__":
    main()
