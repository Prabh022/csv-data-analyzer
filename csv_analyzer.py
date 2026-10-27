"""csv-data-analyzer: summarize a CSV file from the command line.

For each column it reports:
  - numeric columns: value count, missing count, min, max, mean
  - text columns: value count, missing count, unique count, sample values

A column counts as numeric only when every non-empty value parses as a
number. Empty cells are counted as missing, never treated as zero.

Usage:
    python csv_analyzer.py data.csv
    python csv_analyzer.py data.csv --column price

Standard library only.
"""

import argparse
import csv
import sys
from collections import Counter


def _is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def analyze_rows(fieldnames, rows):
    """Return a summary dict for already-read CSV rows.

    fieldnames: list of column names (header row).
    rows: list of dicts mapping column name -> cell string.
    """
    summary = {"row_count": len(rows), "columns": {}}
    for name in fieldnames:
        values = [row.get(name, "") for row in rows]
        present = [v for v in values if v != ""]
        missing = len(values) - len(present)
        info = {"values": len(present), "missing": missing}
        if present and all(_is_number(v) for v in present):
            numbers = [float(v) for v in present]
            info["type"] = "numeric"
            info["min"] = min(numbers)
            info["max"] = max(numbers)
            info["mean"] = sum(numbers) / len(numbers)
        else:
            info["type"] = "text"
            info["unique"] = len(set(present))
            info["sample"] = [v for v, _ in Counter(present).most_common(3)]
        summary["columns"][name] = info
    return summary


def analyze_file(path):
    """Read a CSV file and return its summary, or None if it has no data."""
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            return None
        rows = list(reader)
    if not rows:
        return None
    return analyze_rows(reader.fieldnames, rows)


def format_report(summary, only_column=None):
    """Render a summary dict as plain text."""
    lines = ["Rows: %d" % summary["row_count"], ""]
    names = [only_column] if only_column else summary["columns"]
    for name in names:
        info = summary["columns"].get(name)
        if info is None:
            lines.append("%s: column not found" % name)
            continue
        lines.append("%s (%s): %d values, %d missing"
                     % (name, info["type"], info["values"], info["missing"]))
        if info["type"] == "numeric":
            lines.append("  min %.2f, max %.2f, mean %.2f"
                         % (info["min"], info["max"], info["mean"]))
        else:
            lines.append("  unique: %d, sample: %s"
                         % (info["unique"], ", ".join(info["sample"])))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Summarize a CSV file: row counts and per-column stats.")
    parser.add_argument("file", help="path to the CSV file")
    parser.add_argument("--column", help="show only this column")
    args = parser.parse_args(argv)

    try:
        summary = analyze_file(args.file)
    except FileNotFoundError:
        print("Error: file not found: %s" % args.file, file=sys.stderr)
        return 1
    except (OSError, csv.Error) as exc:
        print("Error: could not read %s: %s" % (args.file, exc),
              file=sys.stderr)
        return 1

    if summary is None:
        print("No data rows found in %s" % args.file)
        return 0
    if args.column and args.column not in summary["columns"]:
        print("Error: column not found: %s" % args.column, file=sys.stderr)
        return 1
    print(format_report(summary, args.column))
    return 0


if __name__ == "__main__":
    sys.exit(main())
