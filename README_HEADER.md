# LeetCode Crawler

## Description

A Web Crawler Scraping LeetCode Problems info such as Difficulties, Related Questions and Topics.

## Data

[Main Data CSV](./Data/leetcode_problem.csv)

[Problems Table Markdown](./Data/problems.md)

[Problems Table HTML](./Data/problems.html)

## Requirements

- `python3`
- [requests](https://requests.readthedocs.io/en/master/)
- [pandas](https://pandas.pydata.org/)

```bash
pip install requests
pip install pandas
```

## Usage

### Options

Top Level: [main.py](./main.py)

```
usage: Scrape Extra Info [-h] [-m] [-y] [-t] [-r]

optional arguments:
  -h, --help          show this help message and exit
  -m, --multiprocess  Use Multiprocessing (utilize as much cores as possible)
  -y, --yield_        Use Yield when Sending requests
  -t, --table         Generate Table
  -r, --readme        Generate README
```

### Examples

```bash
python main.py -m -t -r     # recommended, otherwise data may not always be up to date
```

## All Problems
