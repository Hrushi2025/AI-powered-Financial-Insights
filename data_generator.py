import os  # Import os to handle directories and file paths
import csv  # Import csv (not strictly used here, but often for CSV writing)
import random  # Import random for random number generation
from datetime import datetime, timedelta  # Import datetime and timedelta for date calculations
import numpy as np  # Import numpy for numeric operations, random distributions
import pandas as pd  # Import pandas for DataFrame operations


DATA_DIR = "data"  # Folder where generated CSV files will be saved
NUM_USERS = 5  # Number of synthetic users to generate
DAYS = 180  # Number of days of historical data
START_DATE = datetime.now().date() - timedelta(days=DAYS-1)  # Start date of data (180 days ago)

os.makedirs(DATA_DIR, exist_ok=True)  # Create data directory if it doesn't exist


# 1) Generate users.csv
users = []  # Initialize empty list to store user data
for i in range(1, NUM_USERS+1):  # Loop over user IDs
    users.append({
        "user_id": i,  # Assign user ID
        "name": f"user_{i}",  # Assign username
        "starting_balance": round(random.uniform(200, 2000), 2)  # Random starting balance between 200-2000
    })
users_df = pd.DataFrame(users)  # Convert list of users to DataFrame
users_df.to_csv(os.path.join(DATA_DIR, "users.csv"), index=False)  # Save as CSV
print("Wrote:", os.path.join(DATA_DIR, "users.csv"))  # Print confirmation


# 2) Generate transactions.csv
CATEGORIES = ["groceries", "rent", "entertainment", "utilities", "travel", "transfer", "deposit", "salary", "subscription"]  # Transaction categories
transactions = []  # Initialize list to store transactions
trans_id = 1  # Initialize transaction ID counter

# Loop through each day in history
for day_offset in range(DAYS):
    date = START_DATE + timedelta(days=day_offset)  # Current date
    for user in users:  # Loop through each user
        # Monthly salary deposit (every 30 days, 3rd day)
        if (day_offset % 30) == 2:
            amount = round(random.uniform(800, 3000), 2)
            transactions.append({
                "transaction_id": trans_id,
                "user_id": user["user_id"],
                "timestamp": f"{date} 09:00:00",
                "amount": amount,
                "category": "salary",
                "type": "deposit",
                "merchant": "employer"
            })
            trans_id += 1
        # Random deposits
        if random.random() < 0.05:
            amount = round(random.uniform(50, 1000), 2)
            transactions.append({
                "transaction_id": trans_id,
                "user_id": user["user_id"],
                "timestamp": f"{date} 11:00:00",
                "amount": amount,
                "category": "deposit",
                "type": "deposit",
                "merchant": "bank_transfer"
            })
            trans_id += 1
        # Random daily spending transactions
        num_spends = np.random.poisson(0.9)  # Number of spends per day follows Poisson distribution
        for _ in range(num_spends):
            cat = random.choices(CATEGORIES, weights=[30,5,10,10,5,3,3,2,5])[0]  # Weighted category choice
            if cat == "rent":
                amt = round(random.uniform(400, 1200),2)
                ttype = "spend"
            elif cat == "salary":
                continue  # Skip, salary handled separately
            elif cat == "deposit":
                amt = round(random.uniform(20, 400),2)
                ttype = "deposit"
            elif cat == "transfer":
                amt = round(random.uniform(50, 800),2)
                ttype = "transfer"
            else:
                amt = round(abs(np.random.normal(50, 30)),2) + 1  # Normal distribution for other categories
                ttype = "spend"
            transactions.append({
                "transaction_id": trans_id,
                "user_id": user["user_id"],
                "timestamp": f"{date} {random.randint(8,22)}:{random.randint(0,59):02d}:00",  # Random time during day
                "amount": amt,
                "category": cat,
                "type": ttype,
                "merchant": f"merchant_{random.randint(1,30)}"
            })
            trans_id += 1

# Convert transactions list to DataFrame and save CSV
trans_df = pd.DataFrame(transactions)
trans_df.to_csv(os.path.join(DATA_DIR, "transactions.csv"), index=False)
print("Wrote:", os.path.join(DATA_DIR, "transactions.csv"))


# 3) Generate prices.csv for assets
assets = ["gold", "silver", "bitcoin"]  # Assets to generate prices for
price_rows = []  # Initialize list to store price records
np.random.seed(0)  # Seed for reproducibility

for i in range(DAYS):
    date = START_DATE + timedelta(days=i)  # Current date
    for asset in assets:
        base = {"gold":1800.0, "silver":22.0, "bitcoin":40000.0}[asset]  # Base price
        noise = np.random.normal(0, 1)  # Random noise for realism
        price = base * (1 + 0.0006*i) + noise * (base * 0.005)  # Simulate price trend + noise
        price = max(0.01, float(round(price, 2)))  # Avoid negative prices, round to 2 decimals
        price_rows.append({"date": str(date), "asset": asset, "price": price})  # Append to list

prices_df = pd.DataFrame(price_rows)  # Convert price list to DataFrame
prices_df.to_csv(os.path.join(DATA_DIR, "prices.csv"), index=False)  # Save CSV
print("Wrote:", os.path.join(DATA_DIR, "prices.csv"))


print("Data generation complete. Files in ./data")  # Final confirmation message
