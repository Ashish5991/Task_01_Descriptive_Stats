#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


FILE_PATH = "fb_ads_president_scored_anon.csv"


def print_section(title):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)


def load_dataset(file_path):
    """
    Load CSV into a DataFrame.
    Keep raw values first so we can inspect how Pandas infers types.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def basic_structure(df):
    print_section("BASIC DATASET STRUCTURE")

    print(f"Shape: {df.shape}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn names:")
    for col in df.columns:
        print(f" - {col}")

    print("\nData types:")
    print(df.dtypes)

    print_section("DATAFRAME INFO")
    df.info()


def summary_statistics(df):
    print_section("SUMMARY STATISTICS - NUMERIC COLUMNS")
    numeric_df = df.select_dtypes(include=["number"])

    if numeric_df.shape[1] == 0:
        print("No numeric columns detected by Pandas.")
    else:
        print(numeric_df.describe())

    print_section("SUMMARY STATISTICS - NON-NUMERIC COLUMNS")
    non_numeric_df = df.select_dtypes(exclude=["number"])

    if non_numeric_df.shape[1] == 0:
        print("No non-numeric columns detected by Pandas.")
    else:
        print(non_numeric_df.describe(include="all"))


def missing_value_analysis(df):
    print_section("MISSING VALUE ANALYSIS")

    missing_counts = df.isna().sum()
    missing_percentages = (missing_counts / len(df)) * 100

    missing_summary = pd.DataFrame({
        "missing_count": missing_counts,
        "missing_percentage": missing_percentages.round(2)
    }).sort_values(by="missing_count", ascending=False)

    print(missing_summary)


def categorical_analysis(df, top_n=5):
    print_section("CATEGORICAL COLUMN ANALYSIS")

    categorical_cols = df.select_dtypes(exclude=["number"]).columns

    if len(categorical_cols) == 0:
        print("No categorical/non-numeric columns detected by Pandas.")
        return

    for col in categorical_cols:
        print("\n" + "-" * 100)
        print(f"Column: {col}")
        print("-" * 100)

        non_null_count = df[col].notna().sum()
        unique_count = df[col].nunique(dropna=True)

        print(f"Non-null count : {non_null_count}")
        print(f"Unique values  : {unique_count}")

        print("\nTop values by frequency:")
        value_counts = df[col].value_counts(dropna=True).head(top_n)

        if value_counts.empty:
            print("No non-null values.")
        else:
            print(value_counts)


def clean_numeric_series(series):
    """
    Try to convert messy numeric-looking text into numeric.
    Handles:
    - commas: 1,234
    - currency: $1,234.50
    - percentages: 45%
    - accounting negatives: (123.45)
    If conversion fails, value becomes NaN.
    """
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce")

    cleaned = (
        series.astype(str)
        .str.strip()
        .replace({
            "": np.nan,
            "na": np.nan,
            "n/a": np.nan,
            "null": np.nan,
            "none": np.nan,
            "nan": np.nan,
            "missing": np.nan,
            "-": np.nan
        })
    )

    # accounting negatives: (123) -> -123
    cleaned = cleaned.str.replace(r"^\((.*)\)$", r"-\1", regex=True)

    # remove $, commas, %
    cleaned = cleaned.str.replace(",", "", regex=False)
    cleaned = cleaned.str.replace("$", "", regex=False)
    cleaned = cleaned.str.replace("%", "", regex=False)

    return pd.to_numeric(cleaned, errors="coerce")


def numeric_analysis_with_conversion(df):
    """
    This is useful because some numeric columns may come in as object dtype.
    We inspect every column and see whether it can reasonably behave like numeric.
    """
    print_section("NUMERIC ANALYSIS WITH EXPLICIT CONVERSION")

    numeric_summary_rows = []

    for col in df.columns:
        converted = clean_numeric_series(df[col])

        non_null_original = df[col].notna().sum()
        numeric_count = converted.notna().sum()

        # Heuristic: if at least 80% of non-null values can become numeric,
        # treat the column as numeric-like for analysis.
        ratio = (numeric_count / non_null_original) if non_null_original > 0 else 0

        if ratio >= 0.8 and numeric_count > 0:
            numeric_summary_rows.append({
                "column": col,
                "non_null_original": non_null_original,
                "numeric_count_after_conversion": numeric_count,
                "conversion_ratio": round(ratio, 3),
                "mean": converted.mean(),
                "min": converted.min(),
                "max": converted.max(),
                "std": converted.std(),      # sample std by default
                "median": converted.median()
            })

    if not numeric_summary_rows:
        print("No numeric-like columns found using explicit conversion.")
        return pd.DataFrame()

    numeric_summary_df = pd.DataFrame(numeric_summary_rows)
    print(numeric_summary_df.to_string(index=False))
    return numeric_summary_df


def pandas_numeric_stats_native(df):
    """
    Native Pandas numeric stats only on columns already inferred as numeric.
    """
    print_section("PANDAS NATIVE NUMERIC STATS")

    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(numeric_cols) == 0:
        print("No native numeric columns detected.")
        return pd.DataFrame()

    rows = []
    for col in numeric_cols:
        s = df[col].dropna()
        rows.append({
            "column": col,
            "count": s.count(),
            "mean": s.mean(),
            "min": s.min(),
            "max": s.max(),
            "std": s.std(),
            "median": s.median()
        })

    result = pd.DataFrame(rows)
    print(result.to_string(index=False))
    return result

def main():
    df = load_dataset(FILE_PATH)

    if df is None:
        return

    basic_structure(df)
    summary_statistics(df)
    missing_value_analysis(df)
    categorical_analysis(df, top_n=5)

    native_numeric = pandas_numeric_stats_native(df)
    converted_numeric = numeric_analysis_with_conversion(df)


if __name__ == "__main__":
    main()

