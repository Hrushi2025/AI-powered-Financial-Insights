import os
import pandas as pd

# Data directory
DATA_DIR = "data"


def load_users():
    path = os.path.join(DATA_DIR, "users.csv")
    return pd.read_csv(path)


def load_transactions():
    path = os.path.join(DATA_DIR, "transactions.csv")
    df = pd.read_csv(path, parse_dates=["timestamp"])
    # Ensure types
    df["amount"] = df["amount"].astype(float)
    return df


def load_prices():
    path = os.path.join(DATA_DIR, "prices.csv")
    df = pd.read_csv(path, parse_dates=["date"])  # date only
    df = df.sort_values(["asset", "date"]).reset_index(drop=True)
    return df