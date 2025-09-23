import pandas as pd


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
    df = daily_features.copy()
    if user_id is not None:
        df = df[df['user_id'] == user_id]

    lines = []
    for _, r in df.iterrows():
        uid = r['user_id']
        date = r['date']
        spend = r['spend']
        deposit = r['deposit']
        savings_rate = r.get('savings_rate', 0)

        anomalies_count = anomalies_tx[
            (anomalies_tx['user_id'] == uid)
            & (anomalies_tx['timestamp'].dt.date == pd.to_datetime(date).date())
            & (anomalies_tx['is_anomaly'])
        ].shape[0]

        text = (
            f"User {uid} | {date} — Spent: ₹{spend:.2f}, "
            f"Deposited: ₹{deposit:.2f}, Savings rate: {savings_rate:.2f}, "
            f"Anomalies: {anomalies_count}"
        )

        lines.append({
            'user_id': uid,
            'date': date,
            'summary': text
        })

    return pd.DataFrame(lines)


def compose_weekly_summary(weekly_agg):
    """
    Generate weekly summary strings per user.

    Args:
        weekly_agg (pd.DataFrame): DataFrame with ['user_id', 'week', 'spend', 'deposit', 'net']

    Returns:
        pd.DataFrame: Summary lines with ['user_id', 'week', 'summary']
    """
    lines = []
    for _, r in weekly_agg.iterrows():
        text = (
            f"User {r['user_id']} | Week starting {r['week']} — "
            f"Spend: ₹{r['spend']:.2f}, Deposits: ₹{r['deposit']:.2f}, Net: ₹{r['net']:.2f}"
        )

        lines.append({
            'user_id': r['user_id'],
            'week': r['week'],
            'summary': text
        })

    return pd.DataFrame(lines)