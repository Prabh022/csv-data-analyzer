# Changes

## 2026-11-03 — Standard deviation for numeric columns

- `csv_analyzer.py`: numeric columns now also report the population
  standard deviation (missing cells excluded first; a single value gives
  0.0). The report line now reads
  `min, max, mean, median, stddev`.
- `tests/test_analyzer.py`: 3 new tests (population stddev, single value,
  missing values ignored) — 14 tests total, all passing.
- Sample output in the README updated with the real values
  (price stddev 47.16, quantity stddev 100.31).

## 2026-10-31 — Median for numeric columns

- `csv_analyzer.py`: numeric columns now also report the median (middle
  value, or the average of the two middle values for an even count).
  Missing cells are excluded before the median is computed.
- `tests/test_analyzer.py`: 3 new tests (odd count, even count, missing
  values ignored) — 11 tests total, all passing.

## 2026-10-27 — Initial release

- `csv_analyzer.py`: summarize a CSV file — row count plus per-column
  numeric stats (min, max, mean) or text stats (unique count, samples).
  Missing cells counted, never treated as zero.
- `sample.csv`: small fictional store dataset for demo use.
- `tests/test_analyzer.py`: 8 automated tests, all passing.
