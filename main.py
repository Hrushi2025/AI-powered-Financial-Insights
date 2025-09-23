import os  # For directory and path management
import pandas as pd  # For data handling

# Importing functions from other modules in the project
from etl import load_users, load_transactions, load_prices
from features import daily_user_aggregates, weekly_user_aggregates, add_rolling_features
from anomaly import transaction_zscore_anomalies, daily_net_anomalies
from budget import category_monthly_budget, smart_overall_budget
from investment import asset_momentum, investment_recommendations
from summaries import compose_daily_summary, compose_weekly_summary

# Output directory to save results
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # Create output folder if it doesn't exist

# Loading data from CSV files
print("Loading data...")
users = load_users()           # Load users.csv into DataFrame
transactions = load_transactions()   # Load transactions.csv into DataFrame
prices = load_prices()         # Load prices.csv into DataFrame

# Compute daily aggregates
print("Computing daily aggregates...")
daily = daily_user_aggregates(transactions)  # Summarize daily user transactions
daily.to_csv(os.path.join(OUTPUT_DIR, 'daily_aggregates.csv'), index=False)  # Save CSV
print('Saved daily_aggregates.csv')

# Add rolling features for better analysis
print('Adding rolling features...')
daily_feat = add_rolling_features(daily)  # Compute 7-day rolling averages & savings rate
daily_feat.to_csv(os.path.join(OUTPUT_DIR, 'daily_features.csv'), index=False)
print('Saved daily_features.csv')

# Compute weekly aggregates
print('Weekly aggregates...')
wk = weekly_user_aggregates(daily)  # Summarize weekly user transactions
wk.to_csv(os.path.join(OUTPUT_DIR, 'weekly_aggregates.csv'), index=False)
print('Saved weekly_aggregates.csv')

# Detect anomalies at the transaction level using z-score
print('Detecting anomalies (transaction-level)...')
anom_tx = transaction_zscore_anomalies(transactions)  # Flag unusual transactions
anom_tx.to_csv(os.path.join(OUTPUT_DIR, 'anomalies_transactions.csv'), index=False)
print('Saved anomalies_transactions.csv')

# Detect anomalies in daily net balance
print('Detecting anomalies (daily net)...')
anom_daily = daily_net_anomalies(daily)  # Flag unusual daily net movements
anom_daily.to_csv(os.path.join(OUTPUT_DIR, 'anomalies_daily.csv'), index=False)
print('Saved anomalies_daily.csv')

# Compute category-wise monthly budget suggestions
print('Budget suggestions by category...')
bud_cat = category_monthly_budget(transactions)  # Propose budget per category per user
bud_cat.to_csv(os.path.join(OUTPUT_DIR, 'budgets_by_category.csv'), index=False)
print('Saved budgets_by_category.csv')

# Compute overall smart budget per user
print('Smart overall budgets...')
bud_overall = smart_overall_budget(daily_feat)  # Suggest overall monthly budget per user
bud_overall.to_csv(os.path.join(OUTPUT_DIR, 'budgets_overall.csv'), index=False)
print('Saved budgets_overall.csv')

# Compute asset momentum & investment recommendations
print('Asset momentum & investment recommendations...')
asset_mom = asset_momentum(prices)  # Analyze recent asset trends (7d/30d % changes)
asset_mom.to_csv(os.path.join(OUTPUT_DIR, 'asset_momentum.csv'), index=False)
print('Saved asset_momentum.csv')

# Prepare user surplus data for generating investment recommendations
df_surplus = daily_feat.groupby('user_id').agg({'savings_rate':'mean'}).reset_index()
recs = investment_recommendations(df_surplus, asset_mom)  # Generate investment advice
if not recs.empty:
    recs.to_csv(os.path.join(OUTPUT_DIR, 'recommendations.csv'), index=False)
    print('Saved recommendations.csv')
else:
    print('No recommendations generated for given synthetic data and rules (this can happen).')

# Produce readable daily summaries
print('Producing readable summaries...')
daily_summ = compose_daily_summary(daily_feat, anom_tx)  # Combine features & anomalies
daily_summ.to_csv(os.path.join(OUTPUT_DIR, 'daily_summaries.csv'), index=False)
print('Saved daily_summaries.csv')

# Produce readable weekly summaries
weekly_summ = compose_weekly_summary(wk)
weekly_summ.to_csv(os.path.join(OUTPUT_DIR, 'weekly_summaries.csv'), index=False)
print('Saved weekly_summaries.csv')

# Final message after pipeline completion
print('\nPipeline finished. Check the ./output folder for CSVs.')
