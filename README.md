# csv-data-analyzer

A small command-line tool that summarizes a CSV file: how many rows it has
and, for each column, basic stats. Numeric columns get count, missing count,
min, max, mean, median, and standard deviation (population). Text columns get count, missing count, unique count,
and the most common values. Empty cells are counted as missing, never as
zero. A column counts as numeric only when every non-empty value parses as
a number.

Standard library only — no packages to install. Python 3.8+.

## Usage

```sh
python csv_analyzer.py sample.csv
python csv_analyzer.py sample.csv --column price
```

Sample output for `sample.csv`:

```
Rows: 8

product (text): 8 values, 0 missing
  unique: 5, sample: Notebook, Pen, Mug
category (text): 8 values, 0 missing
  unique: 3, sample: Stationery, Kitchen, Home
price (numeric): 8 values, 0 missing
  min 1.25, max 149.00, mean 25.56, median 7.25, stddev 47.16
quantity (numeric): 7 values, 1 missing
  min 5.00, max 300.00, mean 111.43, median 80.00, stddev 100.31
region (text): 8 values, 0 missing
  unique: 4, sample: North, South, East
```

## Tests

```sh
python -m unittest discover -s tests -v
```

14 tests, covering numeric stats (including median and standard
deviation), missing-value handling,
text columns, mixed-type columns, and report formatting.

## Sample data

`sample.csv` is small fictional store data, made up for demo purposes.
