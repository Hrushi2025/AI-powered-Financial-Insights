import pandas as pd  # Import pandas library for data manipulation


# Function to calculate category-wise monthly budgets based on past spending
def category_monthly_budget(transactions, recent_months=3):
    df = transactions.copy()  # Make a copy to avoid modifying the original DataFrame
    df["date"] = pd.to_datetime(df["timestamp"]).dt.date  # Extract date from timestamp
    df["month"] = pd.to_datetime(df["timestamp"]).dt.to_period("M")  # Extract month (YYYY-MM) from timestamp

    # Consider only spending transactions (exclude deposits, salary, transfers)
    spend = df[df["type"] == "spend"]

    # Aggregate total spending per user, category, and month
    agg = spend.groupby(["user_id", "category", "month"])["amount"].sum().reset_index()

    # Copy the aggregated data (optional, for clarity)
    agg_recent = agg.copy()

    # Compute average monthly spend per user per category across months
    budgets = (
        agg_recent.groupby(["user_id", "category"])["amount"]  # Group by user and category
        .mean()  # Take mean across months
        .reset_index()  # Convert grouped result back to DataFrame
        .rename(columns={"amount": "avg_monthly_spend"})  # Rename column to meaningful name
    )

    # Add 5% slack to propose budget slightly above average spending
    budgets["proposed_budget"] = (budgets["avg_monthly_spend"] * 1.05).round(2)

    return budgets  # Return DataFrame with avg_monthly_spend and proposed_budget


# Function to compute an overall smart monthly budget per user
def smart_overall_budget(daily_features):
    # Use rolling features (7-day average spend) to estimate monthly budget
    df = daily_features.copy()  # Copy input to avoid modifying original
    df["date"] = pd.to_datetime(df["date"])  # Ensure 'date' column is datetime

    # Aggregate by user: take last 7-day average spend and mean savings_rate
    agg = df.groupby("user_id").agg({
        "spend_7d_avg": "last",  # Use most recent 7-day average spending
        "savings_rate": "mean"   # Average savings rate over all days
    }).reset_index()

    # Base estimated monthly budget = 30 times 7-day average spend
    agg["estimated_monthly_spend"] = (agg["spend_7d_avg"] * 30).round(2)

    # Adjust budget based on savings behavior:
    # If savings_rate < 0.1 (i.e., low savings), reduce budget by 10%
    agg["recommended_monthly_budget"] = agg.apply(
        lambda r: round(r["estimated_monthly_spend"] * 0.9, 2)
        if r["savings_rate"] < 0.1
        else round(r["estimated_monthly_spend"] * 1.0, 2),  # Otherwise keep estimated spend
        axis=1
    )

    # Return relevant columns
    return agg[[
        "user_id", "estimated_monthly_spend", "savings_rate", "recommended_monthly_budget"
    ]]
