import os  # Import os to handle file paths
import pandas as pd  # Import pandas for data handling


# Directory where CSV data files are stored
DATA_DIR = "data"


# Function to load users.csv
def load_users():
    path = os.path.join(DATA_DIR, "users.csv")  # Construct file path to users.csv
    return pd.read_csv(path)  # Read CSV into pandas DataFrame and return


# Function to load transactions.csv
def load_transactions():
    path = os.path.join(DATA_DIR, "transactions.csv")  # Construct file path to transactions.csv
    df = pd.read_csv(path, parse_dates=["timestamp"])  # Read CSV and parse 'timestamp' column as datetime
    # Ensure 'amount' column is float type for calculations
    df["amount"] = df["amount"].astype(float)
    return df  # Return the transactions DataFrame


# Function to load prices.csv
def load_prices():
    path = os.path.join(DATA_DIR, "prices.csv")  # Construct file path to prices.csv
    df = pd.read_csv(path, parse_dates=["date"])  # Read CSV and parse 'date' column as datetime
    df = df.sort_values(["asset", "date"]).reset_index(drop=True)  # Sort by asset and date, reset index
    return df  # Return the prices DataFrame
