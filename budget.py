import pandas as pd


def category_monthly_budget(transactions, recent_months=3):
    df = transactions.copy()
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date
    df["month"] = pd.to_datetime(df["timestamp"]).dt.to_period("M")


    # Consider only spending transactions
    spend = df[df["type"] == "spend"]

    # Sum per user, category, and month
    agg = spend.groupby(["user_id", "category", "month"])["amount"].sum().reset_index()

    # Average across recent months
    agg_recent = agg.copy()
    budgets = (
        agg_recent.groupby(["user_id", "category"])["amount"]
        .mean()
        .reset_index()
        .rename(columns={"amount": "avg_monthly_spend"})
    )

    # Proposed budget with a 5% slack
    budgets["proposed_budget"] = (budgets["avg_monthly_spend"] * 1.05).round(2)

    return budgets


def smart_overall_budget(daily_features):
    # Use 30-day rolling spend to suggest overall monthly budget
    df = daily_features.copy()
    df["date"] = pd.to_datetime(df["date"])

    agg = df.groupby("user_id").agg({
        "spend_7d_avg": "last",
        "savings_rate": "mean"
    }).reset_index()

    # Base monthly budget estimate = 30 * spend_7d_avg
    agg["estimated_monthly_spend"] = (agg["spend_7d_avg"] * 30).round(2)

    # If savings_rate < 0.1, propose cutting 10% of budget
    agg["recommended_monthly_budget"] = agg.apply(
        lambda r: round(r["estimated_monthly_spend"] * 0.9, 2)
        if r["savings_rate"] < 0.1
        else round(r["estimated_monthly_spend"] * 1.0, 2),
        axis=1
    )

    return agg[[
        "user_id", "estimated_monthly_spend", "savings_rate", "recommended_monthly_budget"
    ]]