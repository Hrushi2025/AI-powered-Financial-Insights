import pandas as pd
import numpy as np


def transaction_zscore_anomalies(transactions, z_thresh=3.0):
    df = transactions.copy()
    df["abs_amount"] = df["amount"].abs()

    out = []
    for uid, g in df.groupby("user_id"):
        mu = g["abs_amount"].mean()
        sigma = g["abs_amount"].std(ddof=0)

        if sigma == 0 or np.isnan(sigma):
            g["z"] = 0.0
        else:
            g["z"] = (g["abs_amount"] - mu) / sigma

        g["is_anomaly"] = g["z"].abs() > z_thresh
        out.append(g)

    res = pd.concat(out).sort_values(["user_id", "timestamp"])

    return res[[
        "transaction_id", "user_id", "timestamp", "amount",
        "category", "type", "merchant", "z", "is_anomaly"
    ]]


def daily_net_anomalies(daily_agg, z_thresh=3.0):
    df = daily_agg.copy()
    out = []

    for uid, g in df.groupby("user_id"):
        mu = g["net"].mean()
        sigma = g["net"].std(ddof=0)

        if sigma == 0 or np.isnan(sigma):
            g["z_net"] = 0.0
        else:
            g["z_net"] = (g["net"] - mu) / sigma

        g["is_anomaly"] = g["z_net"].abs() > z_thresh
        out.append(g)

    res = pd.concat(out).sort_values(["user_id", "date"])
    return res