# csv-data-analyzer

A small command-line tool that summarizes a CSV file: how many rows it has
and, for each column, basic stats. Numeric columns get count, missing count,
min, max, and mean. Text columns get count, missing count, unique count,
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
  min 1.25, max 149.00, mean 25.56
quantity (numeric): 7 values, 1 missing
  min 5.00, max 300.00, mean 111.43
region (text): 8 values, 0 missing
  unique: 4, sample: North, South, East
```

## Tests

```sh
python -m unittest discover -s tests -v
```

8 tests, covering numeric stats, missing-value handling, text columns,
mixed-type columns, and report formatting.

## Sample data

`sample.csv` is small fictional store data, made up for demo purposes.
