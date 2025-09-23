import pandas as pd  # Import pandas for data manipulation


# Function to compute short-term and long-term momentum of assets
def asset_momentum(df, window_short=7, window_long=30):
    df["date"] = pd.to_datetime(df["date"])  # Ensure 'date' column is datetime type
    out = []  # Initialize list to store momentum snapshots per asset

    # Loop through each asset
    for asset, g in df.groupby("asset"):
        g = g.sort_values("date")  # Sort asset data by date ascending
        g["pct_7d"] = g["price"].pct_change(periods=window_short)   # 7-day percentage change
        g["pct_30d"] = g["price"].pct_change(periods=window_long)  # 30-day percentage change

        # Take the latest row as a snapshot of momentum
        latest = g.iloc[-1]
        out.append({
            "asset": asset,                      # Asset name
            "date": latest["date"].date(),       # Latest date
            "price": latest["price"],            # Latest price
            "pct_7d": float(latest["pct_7d"]) if pd.notnull(latest["pct_7d"]) else 0.0,   # 7-day change, 0 if NaN
            "pct_30d": float(latest["pct_30d"]) if pd.notnull(latest["pct_30d"]) else 0.0, # 30-day change, 0 if NaN
        })

    return pd.DataFrame(out)  # Return DataFrame with momentum snapshot for each asset


# Function to generate investment recommendations per user
def investment_recommendations(user_surplus_df, asset_mom):
    # user_surplus_df: DataFrame with user_id and 'savings_rate' or surplus indicator
    # asset_mom: DataFrame from asset_momentum() containing latest price & momentum
    recs = []  # Initialize list to store recommendations

    # Loop through each user
    for _, u in user_surplus_df.iterrows():
        # Loop through each asset
        for _, a in asset_mom.iterrows():
            # Buy signal: asset dropped >3% in 7 days and user has healthy savings_rate (>15%)
            if a["pct_7d"] < -0.03 and u["savings_rate"] > 0.15:
                recs.append({
                    "user_id": u["user_id"],  # User ID
                    "asset": a["asset"],      # Asset name
                    "action": "BUY",          # Recommended action
                    "reason": f"{a['asset']} down {a['pct_7d']*100:.2f}% in 7d and savings_rate {u['savings_rate']:.2f}",  # Explanation
                    "price": a["price"]       # Current price
                })

            # Take profit signal: asset rose >6% in 7 days
            if a["pct_7d"] > 0.06:
                recs.append({
                    "user_id": u["user_id"],  # User ID
                    "asset": a["asset"],      # Asset name
                    "action": "CONSIDER_TAKE_PROFIT",  # Recommended action
                    "reason": f"{a['asset']} up {a['pct_7d']*100:.2f}% in 7d",  # Explanation
                    "price": a["price"]       # Current price
                })

    return pd.DataFrame(recs)  # Return DataFrame with all user-asset recommendations
