"""Tests for csv_analyzer. Run from the project root:

    python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from csv_analyzer import analyze_rows, format_report  # noqa: E402


class TestAnalyzeRows(unittest.TestCase):
    def setUp(self):
        self.fields = ["name", "price", "qty"]
        self.rows = [
            {"name": "Pen", "price": "1.25", "qty": "10"},
            {"name": "Mug", "price": "9.99", "qty": "3"},
            {"name": "Pen", "price": "1.25", "qty": ""},
        ]

    def test_row_count(self):
        summary = analyze_rows(self.fields, self.rows)
        self.assertEqual(summary["row_count"], 3)

    def test_numeric_column_stats(self):
        info = analyze_rows(self.fields, self.rows)["columns"]["price"]
        self.assertEqual(info["type"], "numeric")
        self.assertEqual(info["values"], 3)
        self.assertEqual(info["missing"], 0)
        self.assertAlmostEqual(info["min"], 1.25)
        self.assertAlmostEqual(info["max"], 9.99)
        self.assertAlmostEqual(info["mean"], (1.25 + 9.99 + 1.25) / 3)

    def test_missing_values_not_counted_as_zero(self):
        info = analyze_rows(self.fields, self.rows)["columns"]["qty"]
        self.assertEqual(info["values"], 2)
        self.assertEqual(info["missing"], 1)
        self.assertAlmostEqual(info["mean"], 6.5)

    def test_text_column_stats(self):
        info = analyze_rows(self.fields, self.rows)["columns"]["name"]
        self.assertEqual(info["type"], "text")
        self.assertEqual(info["unique"], 2)
        self.assertIn("Pen", info["sample"])

    def test_mixed_column_is_text(self):
        rows = [{"name": "A", "price": "5", "qty": "x"}]
        info = analyze_rows(self.fields, rows)["columns"]["qty"]
        self.assertEqual(info["type"], "text")

    def test_report_mentions_column_and_stats(self):
        report = format_report(analyze_rows(self.fields, self.rows))
        self.assertIn("Rows: 3", report)
        self.assertIn("price (numeric)", report)
        self.assertIn("name (text)", report)

    def test_report_single_column(self):
        report = format_report(
            analyze_rows(self.fields, self.rows), only_column="price")
        self.assertIn("price (numeric)", report)
        self.assertNotIn("name (text)", report)

    def test_report_unknown_column(self):
        report = format_report(
            analyze_rows(self.fields, self.rows), only_column="nope")
        self.assertIn("column not found", report)


if __name__ == "__main__":
    unittest.main()
