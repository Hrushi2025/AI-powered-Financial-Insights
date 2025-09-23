import pandas as pd  # Import pandas for data manipulation


# Function to compute daily aggregates per user
def daily_user_aggregates(transactions):
    # Create a separate date column from timestamp
    df = transactions.copy()  # Make a copy to avoid modifying original DataFrame
    df["date"] = df["timestamp"].dt.date  # Extract date part of timestamp

    # Aggregate amounts by user, date, and type (spend/deposit/transfer)
    agg = df.groupby(["user_id", "date", "type"])["amount"].sum().reset_index()

    # Pivot the 'type' column to create separate columns for spend, deposit, transfer
    pivot = agg.pivot_table(
        index=["user_id", "date"],  # Rows = user_id and date
        columns="type",  # Columns = transaction type
        values="amount",  # Values = aggregated amount
        fill_value=0  # Fill missing combinations with 0
    ).reset_index()

    # Calculate total net movement: deposits minus spend and transfer
    pivot["net"] = pivot.get("deposit", 0) - pivot.get("spend", 0) - pivot.get("transfer", 0)
    pivot.columns.name = None  # Remove pivot_table generated column name

    return pivot  # Return daily aggregated DataFrame


# Function to compute weekly aggregates per user
def weekly_user_aggregates(daily_agg):
    d = daily_agg.copy()  # Make a copy
    d["date"] = pd.to_datetime(d["date"])  # Ensure date column is datetime
    # Convert date to week period, then get week start date
    d["week"] = d["date"].dt.to_period("W").apply(lambda r: r.start_time.date())

    # Aggregate spend, deposit, transfer, net per user per week
    wk = d.groupby(["user_id", "week"]).agg({
        "spend": "sum",
        "deposit": "sum",
        "transfer": "sum",
        "net": "sum"
    }).reset_index()

    return wk  # Return weekly aggregated DataFrame


# Function to add rolling features to daily aggregates
def add_rolling_features(daily_agg):
    d = daily_agg.copy()  # Copy to avoid modifying original
    d["date"] = pd.to_datetime(d["date"])  # Ensure date column is datetime
    d = d.sort_values(["user_id", "date"])  # Sort by user and date

    # 7-day rolling average of spend
    d["spend_7d_avg"] = d.groupby("user_id")["spend"].transform(
        lambda x: x.rolling(7, min_periods=1).mean()
    )
    # 7-day rolling average of deposit
    d["deposit_7d_avg"] = d.groupby("user_id")["deposit"].transform(
        lambda x: x.rolling(7, min_periods=1).mean()
    )

    # Compute daily savings rate: deposit / (deposit + spend)
    # Guard against divide-by-zero by returning 0 if sum is 0
    d["savings_rate"] = d.apply(
        lambda r: r["deposit"] / (r["deposit"] + r["spend"]) if (r["deposit"] + r["spend"]) > 0 else 0,
        axis=1
    )

    return d  # Return daily features DataFrame with rolling averages and savings_rate
