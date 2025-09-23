import os
import pandas as pd
from etl import load_users, load_transactions, load_prices
from features import daily_user_aggregates, weekly_user_aggregates, add_rolling_features
from anomaly import transaction_zscore_anomalies, daily_net_anomalies
from budget import category_monthly_budget, smart_overall_budget
from investment import asset_momentum, investment_recommendations
from summaries import compose_daily_summary, compose_weekly_summary

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Loading data...")
users = load_users()           # loads users.csv
transactions = load_transactions()   # loads transactions.csv
prices = load_prices()         # loads prices.csv correctly

print("Computing daily aggregates...")
daily = daily_user_aggregates(transactions)
daily.to_csv(os.path.join(OUTPUT_DIR, 'daily_aggregates.csv'), index=False)
print('Saved daily_aggregates.csv')

print('Adding rolling features...')
daily_feat = add_rolling_features(daily)
daily_feat.to_csv(os.path.join(OUTPUT_DIR, 'daily_features.csv'), index=False)
print('Saved daily_features.csv')

print('Weekly aggregates...')
wk = weekly_user_aggregates(daily)
wk.to_csv(os.path.join(OUTPUT_DIR, 'weekly_aggregates.csv'), index=False)
print('Saved weekly_aggregates.csv')

print('Detecting anomalies (transaction-level)...')
anom_tx = transaction_zscore_anomalies(transactions)
anom_tx.to_csv(os.path.join(OUTPUT_DIR, 'anomalies_transactions.csv'), index=False)
print('Saved anomalies_transactions.csv')

print('Detecting anomalies (daily net)...')
anom_daily = daily_net_anomalies(daily)
anom_daily.to_csv(os.path.join(OUTPUT_DIR, 'anomalies_daily.csv'), index=False)
print('Saved anomalies_daily.csv')

print('Budget suggestions by category...')
bud_cat = category_monthly_budget(transactions)
bud_cat.to_csv(os.path.join(OUTPUT_DIR, 'budgets_by_category.csv'), index=False)
print('Saved budgets_by_category.csv')

print('Smart overall budgets...')
bud_overall = smart_overall_budget(daily_feat)
bud_overall.to_csv(os.path.join(OUTPUT_DIR, 'budgets_overall.csv'), index=False)
print('Saved budgets_overall.csv')

print('Asset momentum & investment recommendations...')
asset_mom = asset_momentum(prices)  # use the loaded 'prices' variable
asset_mom.to_csv(os.path.join(OUTPUT_DIR, 'asset_momentum.csv'), index=False)
print('Saved asset_momentum.csv')

# prepare user surplus frame for investment rules
df_surplus = daily_feat.groupby('user_id').agg({'savings_rate':'mean'}).reset_index()
recs = investment_recommendations(df_surplus, asset_mom)
if not recs.empty:
    recs.to_csv(os.path.join(OUTPUT_DIR, 'recommendations.csv'), index=False)
    print('Saved recommendations.csv')
else:
    print('No recommendations generated for given synthetic data and rules (this can happen).')

print('Producing readable summaries...')
daily_summ = compose_daily_summary(daily_feat, anom_tx)
daily_summ.to_csv(os.path.join(OUTPUT_DIR, 'daily_summaries.csv'), index=False)
print('Saved daily_summaries.csv')

weekly_summ = compose_weekly_summary(wk)
weekly_summ.to_csv(os.path.join(OUTPUT_DIR, 'weekly_summaries.csv'), index=False)
print('Saved weekly_summaries.csv')

print('\nPipeline finished. Check the ./output folder for CSVs.')
