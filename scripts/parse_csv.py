#!/usr/bin/env python3
"""Parse and inspect CSV files from the command line."""

import csv
import sys
import argparse
from pathlib import Path


def parse_csv(path: Path, delimiter: str = ',', limit: int | None = None) -> None:
    with path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=delimiter)

        if reader.fieldnames is None:
            print("Error: empty file or no headers", file=sys.stderr)
            sys.exit(1)

        print(f"File   : {path}")
        print(f"Columns: {', '.join(reader.fieldnames)}")
        print()

        rows = []
        for i, row in enumerate(reader):
            if limit is not None and i >= limit:
                break
            rows.append(row)

        if not rows:
            print("(no rows)")
            return

        # Compute column widths
        widths = {col: len(col) for col in reader.fieldnames}
        for row in rows:
            for col in reader.fieldnames:
                widths[col] = max(widths[col], len(row.get(col) or ''))

        header = '  '.join(col.ljust(widths[col]) for col in reader.fieldnames)
        separator = '  '.join('-' * widths[col] for col in reader.fieldnames)
        print(header)
        print(separator)
        for row in rows:
            print('  '.join((row.get(col) or '').ljust(widths[col]) for col in reader.fieldnames))

        print(f"\n{len(rows)} row(s) shown" + (f" (--limit {limit})" if limit else ""))


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse and display CSV files")
    parser.add_argument("files", nargs='+', type=Path, help="CSV file(s) to parse")
    parser.add_argument("-d", "--delimiter", default=',', help="Field delimiter (default: ',')")
    parser.add_argument("-n", "--limit", type=int, default=None, metavar="N",
                        help="Show only the first N rows")
    args = parser.parse_args()

    for i, path in enumerate(args.files):
        if not path.exists():
            print(f"Error: {path} not found", file=sys.stderr)
            sys.exit(1)
        if i > 0:
            print("\n" + "=" * 60 + "\n")
        parse_csv(path, delimiter=args.delimiter, limit=args.limit)


if __name__ == "__main__":
    main()
