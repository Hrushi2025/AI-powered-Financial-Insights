AI-Powered Financial Insights

Project Overview:
This project builds an AI-powered engine to analyze users’ financial activity, detect anomalies, provide budget suggestions, and recommend investment opportunities. It uses synthetic data for wallet transactions, historical asset prices, and user profiles to generate insights.

Features:

Daily and weekly financial summaries per user

Smart budget suggestions based on user patterns

Anomaly detection in transactions and daily net spending

Investment recommendations using asset momentum

Project Structure
AI-Powered-Financial-Insights/
│
├─ data_generator.py       # Generates synthetic users, transactions, and asset prices
├─ main.py                 # Main pipeline that executes all steps and generates CSV outputs
├─ etl.py                  # Functions to load datasets
├─ features.py             # Computes daily and weekly user aggregates and rolling features
├─ anomaly.py              # Detects transaction-level and daily anomalies
├─ budget.py               # Generates category-wise and overall smart budgets
├─ investment.py           # Computes asset momentum and recommends investments
├─ summaries.py            # Creates human-readable daily and weekly summaries
├─ data/                   # Folder for generated CSV datasets
│   ├─ users.csv
│   ├─ transactions.csv
│   └─ prices.csv
└─ output/                 # Folder where pipeline outputs are saved

Step-by-Step Explanation of Each Module
1. data_generator.py

Purpose: Creates synthetic datasets for testing the pipeline.

What it generates:

users.csv → user profile and starting balances

transactions.csv → deposits, salary, spending, and transfers

prices.csv → historical prices for gold, silver, and bitcoin

Why used: No real dataset is available, so synthetic data simulates real financial behavior.

Alternative: Could load real banking data (CSV/SQL) if available.

2. etl.py

Purpose: Handles loading datasets into pandas DataFrames.

Functions:

load_users()

load_transactions()

load_prices()

Why used: Standardizes data loading for reuse in the pipeline.

Alternative: Could integrate directly with databases like MySQL, BigQuery, or Spark.

3. features.py

Purpose: Compute metrics that summarize users’ financial behavior.

Functions:

daily_user_aggregates() → calculates daily spend, deposits, savings rate per user

weekly_user_aggregates() → summarizes weekly spending and net balance

add_rolling_features() → adds rolling averages, trends, or cumulative metrics

Why used: These features are necessary for anomaly detection, budgets, and summaries.

Alternative: Could use advanced statistical features or ML-based feature engineering.

4. anomaly.py

Purpose: Detect unusual transactions or daily net changes.

Functions:

transaction_zscore_anomalies() → flags transactions that deviate significantly

daily_net_anomalies() → flags abnormal daily net balances

Why used: Helps users identify suspicious activity or overspending.

Alternative: Could implement ML-based anomaly detection (Isolation Forest, Autoencoders).

5. budget.py

Purpose: Suggest budgets to users based on spending patterns.

Functions:

category_monthly_budget() → budget per category

smart_overall_budget() → holistic budget for all categories

Why used: Encourages better financial habits and planning.

Alternative: Could implement predictive budgeting using ML regression models.

6. investment.py

Purpose: Suggest investment actions based on historical asset trends.

Functions:

asset_momentum(prices) → computes momentum (trend) of gold, silver, bitcoin

investment_recommendations(df_surplus, asset_mom) → recommends buy/save/transfer

Why used: Guides users on where to invest their surplus.

Alternative: Could use advanced portfolio optimization, CAPM, or AI trading strategies.

7. summaries.py

Purpose: Converts computed metrics into readable summaries.

Functions:

compose_daily_summary(daily_features, anomalies_tx) → per-user daily summary

compose_weekly_summary(weekly_agg) → per-user weekly summary

Why used: Makes outputs human-readable for notifications or dashboards.

Alternative: Could generate HTML dashboards or integrate with Streamlit for real-time UI.

8. main.py

Purpose: Orchestrates the full pipeline:

Load data

Compute daily and weekly aggregates

Add rolling features

Detect anomalies

Generate budgets

Compute investment recommendations

Create summaries

Why used: Single entry point for end-to-end processing.

Alternative: Could be broken into Airflow tasks or a Spark pipeline for large-scale deployment.
