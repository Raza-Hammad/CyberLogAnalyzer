import pandas as pd

def parse_logs(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["is_night"] = df["hour"].apply(lambda x: 1 if x < 6 or x > 22 else 0)
    df["login_failed"] = df["login_status"].apply(lambda x: 1 if x == "failure" else 0)
    return df
