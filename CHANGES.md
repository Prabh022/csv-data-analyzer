# Changes

## 2026-10-27 — Initial release

- `csv_analyzer.py`: summarize a CSV file — row count plus per-column
  numeric stats (min, max, mean) or text stats (unique count, samples).
  Missing cells counted, never treated as zero.
- `sample.csv`: small fictional store dataset for demo use.
- `tests/test_analyzer.py`: 8 automated tests, all passing.
