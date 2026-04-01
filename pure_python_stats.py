#!/usr/bin/env python
# coding: utf-8

# In[9]:


import csv
import math
import statistics
from collections import Counter

MISSING_VALUES = {"", "na", "n/a", "null", "none", "nan", "missing", "-"}


def is_missing(value):
    if value is None:
        return True
    return str(value).strip().lower() in MISSING_VALUES


def clean_string(value):
    if value is None:
        return ""
    return str(value).strip()


def try_parse_number(value):
    """
    Try to convert a value into a float.
    Handles values like:
    - 123
    - 1,234
    - $1,234.56
    - 45%
    - (123.45)  -> negative accounting format
    Returns None if parsing fails.
    """
    if value is None:
        return None

    s = str(value).strip()

    if s == "":
        return None

    lower_s = s.lower()
    if lower_s in MISSING_VALUES:
        return None

    # Remove surrounding whitespace
    s = s.strip()

    # Handle accounting negative numbers like (123.45)
    negative = False
    if s.startswith("(") and s.endswith(")"):
        negative = True
        s = s[1:-1].strip()

    # Remove currency symbols and commas
    s = s.replace(",", "")
    s = s.replace("$", "")
    s = s.replace("€", "")
    s = s.replace("£", "")

    # Handle percentages
    is_percent = False
    if s.endswith("%"):
        is_percent = True
        s = s[:-1].strip()

    try:
        num = float(s)
        if negative:
            num = -num
        if is_percent:
            num = num / 100.0
        return num
    except ValueError:
        return None


def infer_column_type(non_missing_values):
    """
    Infer data type for a column based on non-missing values.
    Rules:
    - all missing -> 'empty'
    - if >= 80% of non-missing values can be parsed as number -> 'numeric'
    - otherwise -> 'categorical/text'
    """
    if not non_missing_values:
        return "empty"

    numeric_count = 0
    for v in non_missing_values:
        if try_parse_number(v) is not None:
            numeric_count += 1

    ratio = numeric_count / len(non_missing_values)

    if ratio == 1.0:
        return "numeric"
    elif ratio >= 0.8:
        return "mostly numeric"
    else:
        return "categorical/text"


def compute_numeric_stats(values):
    """
    values: list of floats
    Returns dictionary of numeric stats.
    """
    result = {
        "count": 0,
        "mean": None,
        "min": None,
        "max": None,
        "std_dev": None,
        "median": None,
    }

    if not values:
        return result

    n = len(values)
    total = sum(values)
    mean_value = total / n
    min_value = min(values)
    max_value = max(values)
    median_value = statistics.median(values)

    # Sample standard deviation if n > 1, else 0.0
    if n > 1:
        variance = sum((x - mean_value) ** 2 for x in values) / (n - 1)
        std_dev = math.sqrt(variance)
    else:
        std_dev = 0.0

    result["count"] = n
    result["mean"] = mean_value
    result["min"] = min_value
    result["max"] = max_value
    result["std_dev"] = std_dev
    result["median"] = median_value
    return result


def compute_categorical_stats(values):
    """
    values: list of cleaned non-missing strings
    Returns dictionary of categorical stats.
    """
    result = {
        "count": 0,
        "unique_count": 0,
        "mode": None,
        "mode_frequency": 0,
        "top_5": [],
    }

    if not values:
        return result

    counter = Counter(values)
    most_common = counter.most_common()

    result["count"] = len(values)
    result["unique_count"] = len(counter)

    if most_common:
        result["mode"] = most_common[0][0]
        result["mode_frequency"] = most_common[0][1]

    result["top_5"] = most_common[:5]
    return result


def format_number(value):
    if value is None:
        return "None"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def load_csv(file_path):
    """
    Load CSV using csv.DictReader.
    Returns:
    - rows: list of dicts
    - fieldnames: list of column names
    """
    with open(file_path, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames if reader.fieldnames else []
    return rows, fieldnames


def analyze_dataset(rows, fieldnames):
    total_rows = len(rows)
    total_columns = len(fieldnames)

    # Prepare column-wise storage
    columns = {field: [] for field in fieldnames}

    for row in rows:
        for field in fieldnames:
            columns[field].append(row.get(field))

    # Dataset-level summary
    print("=" * 80)
    print("DATASET OVERVIEW")
    print("=" * 80)
    print(f"Total row count    : {total_rows}")
    print(f"Total column count : {total_columns}")
    print()

    print("Missing values per column:")
    missing_counts = {}
    for field in fieldnames:
        missing_count = sum(1 for v in columns[field] if is_missing(v))
        missing_counts[field] = missing_count
        print(f"  - {field}: {missing_count}")
    print()

    print("Inferred data type per column:")
    inferred_types = {}
    for field in fieldnames:
        non_missing = [v for v in columns[field] if not is_missing(v)]
        inferred = infer_column_type(non_missing)
        inferred_types[field] = inferred
        print(f"  - {field}: {inferred}")
    print()

    print("=" * 80)
    print("COLUMN ANALYSIS")
    print("=" * 80)

    for field in fieldnames:
        print(f"\nCOLUMN: {field}")
        print("-" * 80)

        raw_values = columns[field]
        non_missing_raw = [v for v in raw_values if not is_missing(v)]
        inferred_type = inferred_types[field]

        print(f"Inferred type      : {inferred_type}")
        print(f"Total values       : {len(raw_values)}")
        print(f"Non-missing values : {len(non_missing_raw)}")
        print(f"Missing values     : {missing_counts[field]}")

        if inferred_type in ("numeric", "mostly numeric"):
            numeric_values = []
            non_numeric_examples = []

            for v in non_missing_raw:
                parsed = try_parse_number(v)
                if parsed is not None:
                    numeric_values.append(parsed)
                else:
                    if len(non_numeric_examples) < 5:
                        non_numeric_examples.append(v)

            stats = compute_numeric_stats(numeric_values)

            print("\nNumeric statistics:")
            print(f"  Count              : {stats['count']}")
            print(f"  Mean               : {format_number(stats['mean'])}")
            print(f"  Minimum            : {format_number(stats['min'])}")
            print(f"  Maximum            : {format_number(stats['max'])}")
            print(f"  Standard deviation : {format_number(stats['std_dev'])}")
            print(f"  Median             : {format_number(stats['median'])}")

            bad_value_count = len(non_missing_raw) - len(numeric_values)
            print(f"  Non-numeric values ignored: {bad_value_count}")
            if non_numeric_examples:
                print(f"  Example bad values       : {non_numeric_examples}")

        else:
            cleaned_values = [clean_string(v) for v in non_missing_raw]
            stats = compute_categorical_stats(cleaned_values)

            print("\nCategorical statistics:")
            print(f"  Count                  : {stats['count']}")
            print(f"  Unique values          : {stats['unique_count']}")
            print(f"  Most frequent value    : {stats['mode']}")
            print(f"  Mode frequency         : {stats['mode_frequency']}")
            print(f"  Top 5 values by freq   :")
            if stats["top_5"]:
                for value, freq in stats["top_5"]:
                    print(f"    - {value}: {freq}")
            else:
                print("    None")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)


def main():
    file_path = "fb_ads_president_scored_anon.csv"

    try:
        rows, fieldnames = load_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")
        print("Make sure the CSV file is in the same folder as this script.")
        return
    except Exception as e:
        print(f"Error while reading CSV: {e}")
        return

    if not fieldnames:
        print("Error: CSV appears to have no header row.")
        return

    analyze_dataset(rows, fieldnames)


if __name__ == "__main__":
    main()

