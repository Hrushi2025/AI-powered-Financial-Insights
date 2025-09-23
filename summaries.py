import pandas as pd  # Import pandas library for data manipulation


# Function to generate daily summary strings per user-day
def compose_daily_summary(daily_features, anomalies_tx, user_id=None):
    """
    Generate daily summary strings per user-day.

    Args:
        daily_features (pd.DataFrame): DataFrame with columns ['user_id', 'date', 'spend', 'deposit', 'savings_rate']
        anomalies_tx (pd.DataFrame): DataFrame with anomaly transactions ['user_id', 'timestamp', 'is_anomaly']
        user_id (optional): Filter for a single user if provided.

    Returns:
        pd.DataFrame: Summary lines with ['user_id', 'date', 'summary']
    """
    df = daily_features.copy()  # Copy the daily features DataFrame to avoid modifying original
    if user_id is not None:
        df = df[df['user_id'] == user_id]  # Filter for a specific user if provided

    lines = []  # Initialize list to store summary rows
    for _, r in df.iterrows():  # Iterate over each row in daily features
        uid = r['user_id']  # Extract user ID
        date = r['date']    # Extract date
        spend = r['spend']  # Extract daily spending
        deposit = r['deposit']  # Extract daily deposit
        savings_rate = r.get('savings_rate', 0)  # Extract savings rate, default to 0 if missing

        # Count number of anomaly transactions for this user on this date
        anomalies_count = anomalies_tx[
            (anomalies_tx['user_id'] == uid)  # Match user
            & (anomalies_tx['timestamp'].dt.date == pd.to_datetime(date).date())  # Match date
            & (anomalies_tx['is_anomaly'])  # Only count flagged anomalies
        ].shape[0]

        # Compose human-readable summary string
        text = (
            f"User {uid} | {date} — Spent: ₹{spend:.2f}, "
            f"Deposited: ₹{deposit:.2f}, Savings rate: {savings_rate:.2f}, "
            f"Anomalies: {anomalies_count}"
        )

        # Append dictionary with summary to the lines list
        lines.append({
            'user_id': uid,
            'date': date,
            'summary': text
        })

    return pd.DataFrame(lines)  # Convert the list of dictionaries to a DataFrame and return


# Function to generate weekly summary strings per user
def compose_weekly_summary(weekly_agg):
    """
    Generate weekly summary strings per user.

    Args:
        weekly_agg (pd.DataFrame): DataFrame with ['user_id', 'week', 'spend', 'deposit', 'net']

    Returns:
        pd.DataFrame: Summary lines with ['user_id', 'week', 'summary']
    """
    lines = []  # Initialize list to store weekly summary rows
    for _, r in weekly_agg.iterrows():  # Iterate over each row in weekly aggregates
        # Compose human-readable summary string for the week
        text = (
            f"User {r['user_id']} | Week starting {r['week']} — "
            f"Spend: ₹{r['spend']:.2f}, Deposits: ₹{r['deposit']:.2f}, Net: ₹{r['net']:.2f}"
        )

        # Append dictionary with summary to the lines list
        lines.append({
            'user_id': r['user_id'],
            'week': r['week'],
            'summary': text
        })

    return pd.DataFrame(lines)  # Convert the list of dictionaries to a DataFrame and return
