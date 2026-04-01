# Findings and Interesting Insights

This analysis explores patterns in Facebook political advertising using a dataset of over 246,000 ads across 40 variables. By combining both a pure Python and Pandas-based approach, the goal was not only to compute statistics but to understand deeper patterns in political messaging, spending behavior, and campaign strategies.

### Overall Data Structure and Consistency

The dataset is large and relatively clean, with 246,745 observations and 40 columns. Missing data is minimal and concentrated in only a few columns such as ad_delivery_stop_time (0.87%), bylines (0.41%), and estimated_audience_size (0.23%).

One important observation is that many fields that appear numeric, such as spend, impressions, and estimated_audience_size, are actually stored as categorical strings representing ranges, for example:
{'lower_bound': '0', 'upper_bound': '99'}

This has a significant impact on analysis and highlights how data representation decisions affect downstream insights.

### Concentration of Political Advertising Activity

A key finding is that political advertising is highly concentrated among a few major actors rather than evenly distributed.

The most active pages in the dataset were:

- Kamala Harris — 55,503 ads
- Donald J. Trump — 23,988 ads
- Joe Biden — 14,822 ads

A small number of organizations dominate the dataset, with the top few accounts contributing a disproportionately large share of ads.

This suggests that Facebook political advertising is not a level playing field, but rather dominated by well-funded campaigns and large organizations.

### Spending Patterns: Many Small Ads, Few Large Ones

Although exact numeric spend values are not directly available, the distribution of spend ranges reveals an important pattern.

The majority of ads fall into the lowest spend category:

($0–$99) → 135,950 ads, which is roughly 55% of all ads

Higher spending brackets appear much less frequently.

This indicates that campaigns rely heavily on high-volume, low-cost advertising strategies, rather than a few expensive ads. In other words, political campaigns appear to optimize for reach through volume, not just high-budget campaigns.

### Temporal Patterns: Clear Campaign Spikes

Ad activity shows a strong concentration around late October 2024.

The most frequent dates were:

Ad creation date: 2024-10-27 — 8,619 ads
Ad delivery start date: 2024-10-28 — 10,089 ads
Ad delivery stop date: 2024-11-05 — 14,222 ads

This clearly suggests that political ad spending intensifies dramatically in the final days leading up to the election. This aligns with real-world campaign behavior where last-minute voter influence is critical.

### Candidate Mentions and Messaging Strategy

The `illuminating_mentions` column reveals how often candidates are referenced.

Most common values were:

* `[]` — 73,205 ads
* `['Donald Trump']` — 53,182 ads
* `['Kamala Harris']` — 31,019 ads
* `['President Trump']` — 14,580 ads
* `['Joe Biden']` — 14,059 ads

This is interesting for two reasons:

1. A large portion of ads do not explicitly mention candidates, suggesting issue-based or indirect messaging.
2. Donald Trump is mentioned significantly more often than others, even when not necessarily being the advertiser.

This suggests that political messaging is not always direct promotion. It often revolves around opposition framing or issue-based narratives.


### Nature of Political Messaging

The dataset includes binary indicators for different message types. These provide insight into how campaigns communicate.

Some important results include:

- `illuminating_msg_type_cta` — about 57%
- `illuminating_msg_type_advocacy` — about 54%
- `illuminating_msg_type_issue` — about 38%
- `illuminating_msg_type_attack` — about 27%
- `illuminating_incivility` — about 18.7%

These results suggest that the most common ad styles were call-to-action, advocacy, and issue-oriented messaging. Attack messaging is present, but it is not the dominant mode. Incivility is also present in a meaningful portion of ads, though still in the minority.


### Topic Distribution: What Campaigns Focus On

Some topics appear significantly more frequently than others:

* **Economy** — about 12%
* **Health** — about 12%
* **Social and cultural issues** — about 8%

Less frequent topics include:

* **Women's issues** — about 1.9%
* **Military** — about 0.7%
* **LGBTQ** — about 0.3%

This suggests that campaigns prioritize broad, high-impact issues such as economy and health over specialized topics.


### Platform Distribution

The vast majority of ads were delivered across both Facebook and Instagram:

* **['Facebook', 'Instagram']** — 214,340 ads, roughly 87%

This indicates that campaigns are leveraging multi-platform distribution to maximize reach.


# Comparison of the Two Approaches

### Do the results agree?
Yes. The pure Python and Pandas approaches produced consistent results for the columns that are truly numeric, especially the binary indicator columns such as:

- illuminating_scam
- illuminating_msg_type_advocacy
- illuminating_msg_type_attack
- illuminating_topic_health
- illuminating_incivility

For these columns, both scripts returned the same values for count, mean, minimum, maximum, standard deviation, and median.

This confirms that the pure Python calculations were implemented correctly and that the Pandas output is consistent with them.

### Why might the results differ?

The main reason results can differ is type inference.

In the pure Python script, each column was manually checked to determine whether it behaved like numeric data or categorical data. In the Pandas script, type detection depended first on how Pandas interpreted the CSV file.

This became especially important for columns like:

- spend
- impressions
- estimated_audience_size

These look numeric in meaning, but because they are stored as strings representing ranges, both approaches treated them as categorical/text instead of standard numeric variables.

Other possible reasons differences might occur include:

- different handling of missing values
- differences in cleaning messy strings
- rounding differences
- whether a script silently ignores invalid values

In this project, the numeric results matched because the truly numeric columns were already clean binary indicators.

### What did the pure Python approach force me to think about?
The pure Python version required more explicit decisions, including:

- how to detect missing values
- how to determine whether a column is numeric or categorical
- how to handle columns that look numeric but are actually stored as strings
- how mean, median, and standard deviation are computed manually
- how to avoid crashing when values are missing or inconsistent

This made the logic of the analysis much more transparent.

### What did Pandas make easier?
The Pandas version made it much faster to:

- load the dataset
- inspect shape and data types
- compute missing values
- generate summary statistics
- view frequency counts
- summarize numeric columns with describe()

Pandas reduced a lot of code and made the workflow much more efficient.

## Dataset

The dataset is not included in this repository.

You can download the dataset from the following source:
[https://drive.google.com/file/d/1gvtvX8fATFrrzraPmTSf205U8u3JExUR/view]

After downloading, place the file in the root directory of this project with the following name:

fb_ads_president_scored_anon.csv

The folder structure should look like this:

Task_01_Descriptive_Stats/
├── pure_python_stats.py
├── pandas_stats.py
├── README.md
├── requirements.txt
└── fb_ads_president_scored_anon.csv
