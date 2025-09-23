import pandas as pd


def asset_momentum(df, window_short=7, window_long=30):
    df["date"] = pd.to_datetime(df["date"])
    out = []

    for asset, g in df.groupby("asset"):
        g = g.sort_values("date")
        g["pct_7d"] = g["price"].pct_change(periods=window_short)
        g["pct_30d"] = g["price"].pct_change(periods=window_long)

        # Latest row for momentum snapshot
        latest = g.iloc[-1]
        out.append({
            "asset": asset,
            "date": latest["date"].date(),
            "price": latest["price"],
            "pct_7d": float(latest["pct_7d"]) if pd.notnull(latest["pct_7d"]) else 0.0,
            "pct_30d": float(latest["pct_30d"]) if pd.notnull(latest["pct_30d"]) else 0.0,
        })

    return pd.DataFrame(out)


def investment_recommendations(user_surplus_df, asset_mom):
    # user_surplus_df: DataFrame with user_id and 'savings_rate' or 'surplus' indicator
    # asset_mom: output from asset_momentum()
    recs = []

    for _, u in user_surplus_df.iterrows():
        for _, a in asset_mom.iterrows():
            # Buy signal: asset drops more than 3% in 7 days, and user has healthy savings_rate
            if a["pct_7d"] < -0.03 and u["savings_rate"] > 0.15:
                recs.append({
                    "user_id": u["user_id"],
                    "asset": a["asset"],
                    "action": "BUY",
                    "reason": f"{a['asset']} down {a['pct_7d']*100:.2f}% in 7d and savings_rate {u['savings_rate']:.2f}",
                    "price": a["price"]
                })

            # Take profit signal: asset rises more than 6% in 7 days
            if a["pct_7d"] > 0.06:
                recs.append({
                    "user_id": u["user_id"],
                    "asset": a["asset"],
                    "action": "CONSIDER_TAKE_PROFIT",
                    "reason": f"{a['asset']} up {a['pct_7d']*100:.2f}% in 7d",
                    "price": a["price"]
                })

    return pd.DataFrame(recs)