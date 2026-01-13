import pandas as pd
from datetime import datetime

BLOCK_FILE = "data/blocked_ips.csv"

def block_ip_if_needed(row):
    """Block an IP if its risk score is high"""
    if row["risk_score"] > 70:
        try:
            blocked = pd.read_csv(BLOCK_FILE)
        except FileNotFoundError:
            blocked = pd.DataFrame(columns=["ip_address", "blocked_at", "reason"])

        if row["ip_address"] not in blocked["ip_address"].values:
            new_row_df = pd.DataFrame([{
                "ip_address": row["ip_address"],
                "blocked_at": datetime.now(),
                "reason": "High risk login detected"
            }])
            blocked = pd.concat([blocked, new_row_df], ignore_index=True)
            try:
                blocked.to_csv(BLOCK_FILE, index=False)
            except PermissionError:
                print(f"Error: Could not write to {BLOCK_FILE}. Is it open?")
