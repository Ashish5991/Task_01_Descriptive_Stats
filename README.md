# Task_01_Descriptive_Stats

## Project Description

This project analyzes a Facebook political advertising dataset using two different approaches:

1. **Pure Python (`pure_python_stats.py`)**
   - Uses only the Python standard library
   - Computes descriptive statistics manually
   - Focuses on understanding how statistics are calculated and how to handle messy real-world data

2. **Pandas (`pandas_stats.py`)**
   - Performs the same analysis using Pandas
   - Uses built-in DataFrame functionality for faster and more concise analysis
   - Helps compare manual statistical computation with library-based analysis

The goal of this project is not just to generate statistics, but to understand:
- how missing values affect analysis
- how data types are inferred
- how categorical and numeric columns should be handled differently
- how results can differ depending on the analysis approach

This dataset contains **246,745 rows and 40 columns**. It includes metadata about Facebook political ads, spending ranges, delivery dates, advertiser information, platform usage, candidate mentions, and multiple binary indicators related to messaging type, topics, and ad tone.

---

## Repository Contents

- `pure_python_stats.py` — descriptive statistics using only the Python standard library
- `pandas_stats.py` — equivalent analysis using Pandas
- `requirements.txt` — dependency list for the Pandas script
- `README.md` — project overview, run instructions, findings, and comparison
- `requirements.txt` - All dependencies
---
