import os
import csv
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

DATA_DIR = "data"
NUM_USERS = 5
DAYS = 180
START_DATE = datetime.now().date() - timedelta(days=DAYS-1)

os.makedirs(DATA_DIR, exist_ok=True)

# 1) users.csv
users = []
for i in range(1, NUM_USERS+1):
    users.append({
        "user_id": i,
        "name": f"user_{i}",
        "starting_balance": round(random.uniform(200, 2000), 2)
    })
users_df = pd.DataFrame(users)
users_df.to_csv(os.path.join(DATA_DIR, "users.csv"), index=False)
print("Wrote:", os.path.join(DATA_DIR, "users.csv"))

# 2) transactions.csv
CATEGORIES = ["groceries", "rent", "entertainment", "utilities", "travel", "transfer", "deposit", "salary", "subscription"]
transactions = []
trans_id = 1

for day_offset in range(DAYS):
    date = START_DATE + timedelta(days=day_offset)
    for user in users:
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
        num_spends = np.random.poisson(0.9)
        for _ in range(num_spends):
            cat = random.choices(CATEGORIES, weights=[30,5,10,10,5,3,3,2,5])[0]
            if cat == "rent":
                amt = round(random.uniform(400, 1200),2)
                ttype = "spend"
            elif cat == "salary":
                continue
            elif cat == "deposit":
                amt = round(random.uniform(20, 400),2)
                ttype = "deposit"
            elif cat == "transfer":
                amt = round(random.uniform(50, 800),2)
                ttype = "transfer"
            else:
                amt = round(abs(np.random.normal(50, 30)),2) + 1
                ttype = "spend"
            transactions.append({
                "transaction_id": trans_id,
                "user_id": user["user_id"],
                "timestamp": f"{date} {random.randint(8,22)}:{random.randint(0,59):02d}:00",
                "amount": amt,
                "category": cat,
                "type": ttype,
                "merchant": f"merchant_{random.randint(1,30)}"
            })
            trans_id += 1

trans_df = pd.DataFrame(transactions)
trans_df.to_csv(os.path.join(DATA_DIR, "transactions.csv"), index=False)
print("Wrote:", os.path.join(DATA_DIR, "transactions.csv"))

# 3) prices.csv
assets = ["gold", "silver", "bitcoin"]
price_rows = []
np.random.seed(0)
for i in range(DAYS):
    date = START_DATE + timedelta(days=i)
    for asset in assets:
        base = {"gold":1800.0, "silver":22.0, "bitcoin":40000.0}[asset]
        noise = np.random.normal(0, 1)
        price = base * (1 + 0.0006*i) + noise * (base * 0.005)
        price = max(0.01, float(round(price, 2)))
        price_rows.append({"date": str(date), "asset": asset, "price": price})

prices_df = pd.DataFrame(price_rows)
prices_df.to_csv(os.path.join(DATA_DIR, "prices.csv"), index=False)
print("Wrote:", os.path.join(DATA_DIR, "prices.csv"))

print("Data generation complete. Files in ./data")