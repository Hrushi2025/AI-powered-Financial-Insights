import pandas as pd   # Import pandas library for data manipulation
import numpy as np    # Import numpy library for numerical computations


# Function to detect transaction-level anomalies using z-score
def transaction_zscore_anomalies(transactions, z_thresh=3.0):
    df = transactions.copy()  # Create a copy of the input DataFrame to avoid modifying original data
    df["abs_amount"] = df["amount"].abs()  # Take absolute value of transaction amounts for anomaly calculation

    out = []  # Initialize a list to store processed data per user
    for uid, g in df.groupby("user_id"):  # Group transactions by each user
        mu = g["abs_amount"].mean()       # Compute mean of absolute amounts for the user
        sigma = g["abs_amount"].std(ddof=0)  # Compute standard deviation (population std) of absolute amounts

        # If standard deviation is zero or NaN, assign z-score zero to avoid division by zero
        if sigma == 0 or np.isnan(sigma):
            g["z"] = 0.0
        else:
            g["z"] = (g["abs_amount"] - mu) / sigma  # Compute z-score for each transaction

        g["is_anomaly"] = g["z"].abs() > z_thresh  # Flag transaction as anomaly if z-score exceeds threshold
        out.append(g)  # Add this user's processed transactions to the output list

    res = pd.concat(out).sort_values(["user_id", "timestamp"])  # Combine all users' transactions and sort by user and time

    # Return only relevant columns including z-score and anomaly flag
    return res[[
        "transaction_id", "user_id", "timestamp", "amount",
        "category", "type", "merchant", "z", "is_anomaly"
    ]]


# Function to detect anomalies in daily net amounts for each user
def daily_net_anomalies(daily_agg, z_thresh=3.0):
    df = daily_agg.copy()  # Copy the input daily aggregates DataFrame
    out = []  # Initialize a list to store processed data per user

    for uid, g in df.groupby("user_id"):  # Group daily aggregates by user
        mu = g["net"].mean()       # Compute mean of daily net values for the user
        sigma = g["net"].std(ddof=0)  # Compute standard deviation (population std) of daily net values

        # If std is zero or NaN, assign z-score 0
        if sigma == 0 or np.isnan(sigma):
            g["z_net"] = 0.0
        else:
            g["z_net"] = (g["net"] - mu) / sigma  # Compute z-score of daily net

        g["is_anomaly"] = g["z_net"].abs() > z_thresh  # Flag day as anomaly if z-score exceeds threshold
        out.append(g)  # Add this user's processed daily data to output

    res = pd.concat(out).sort_values(["user_id", "date"])  # Combine all users' daily data and sort by user and date
    return res  # Return the resulting DataFrame with z-score and anomaly flags
