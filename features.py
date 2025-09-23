import pandas as pd


def daily_user_aggregates(transactions):
    # Create date column
    df = transactions.copy()
    df["date"] = df["timestamp"].dt.date

    # Spending, deposits, transfers per day
    agg = df.groupby(["user_id", "date", "type"])["amount"].sum().reset_index()

    # Pivot types into columns
    pivot = agg.pivot_table(
        index=["user_id", "date"],
        columns="type",
        values="amount",
        fill_value=0
    ).reset_index()

    # Total net balance movement
    pivot["net"] = pivot.get("deposit", 0) - pivot.get("spend", 0) - pivot.get("transfer", 0)
    pivot.columns.name = None

    return pivot


def weekly_user_aggregates(daily_agg):
    d = daily_agg.copy()
    d["date"] = pd.to_datetime(d["date"])
    d["week"] = d["date"].dt.to_period("W").apply(lambda r: r.start_time.date())

    wk = d.groupby(["user_id", "week"]).agg({
        "spend": "sum",
        "deposit": "sum",
        "transfer": "sum",
        "net": "sum"
    }).reset_index()

    return wk


def add_rolling_features(daily_agg):
    d = daily_agg.copy()
    d["date"] = pd.to_datetime(d["date"])
    d = d.sort_values(["user_id", "date"])

    # 7-day rolling averages
    d["spend_7d_avg"] = d.groupby("user_id")["spend"].transform(lambda x: x.rolling(7, min_periods=1).mean())
    d["deposit_7d_avg"] = d.groupby("user_id")["deposit"].transform(lambda x: x.rolling(7, min_periods=1).mean())

    # Savings rate: deposit / (deposit + spend) with divide-by-zero guard
    d["savings_rate"] = d.apply(
        lambda r: r["deposit"] / (r["deposit"] + r["spend"]) if (r["deposit"] + r["spend"]) > 0 else 0,
        axis=1
    )

    return d