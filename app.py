from flask import Flask, render_template, request, redirect
import pandas as pd
import joblib
from datetime import datetime
from collections import defaultdict
from utils.log_parser import parse_logs
from utils.feature_engineering import prepare_features
from utils.risk_scoring import calculate_risk
from utils.ip_blocker import block_ip_if_needed
from utils.alerts import send_alert
from utils.visualization import generate_risk_chart, generate_hour_chart

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Load ML model
try:
    model = joblib.load(app.config["MODEL_PATH"])
except FileNotFoundError:
    print(f"Warning: Model not found at {app.config['MODEL_PATH']}")
    model = None

# Track failed attempts per IP
ip_attempts = defaultdict(int)

# Check if IP is blocked
def is_blocked(ip):
    try:
        blocked = pd.read_csv(app.config["BLOCK_FILE"])
        return ip in blocked["ip_address"].values

    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error reading block file: {e}")
        return False

def process_login_attempt(row):
    """Check risk and block IP if necessary, send alert"""
    ip = row["ip_address"]

    # Extreme risk -> block immediately
    if row["risk_score"] > 85:
        block_ip_if_needed(row)
        send_alert(row)
        return True

    # Medium-high risk -> block after 1 failed attempt
    elif row["risk_score"] > 70 and ip_attempts[ip] >= 1:
        block_ip_if_needed(row)
        send_alert(row)
        return True

    return False

@app.route("/", methods=["GET"])
def home():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        ip_address = request.remote_addr
        device_type = "web"
        location = "unknown"

        # Check if IP is blocked
        if is_blocked(ip_address):
            error = "Your IP is blocked due to suspicious activity."
            return render_template("login.html", error=error)

        # Simulate login attempt
        df = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": username,
            "ip_address": ip_address,
            "login_status": "success" if app.config["USER_DB"].get(username) == password else "failure",
            "device_type": device_type,
            "location": location
        }])

        df = parse_logs(df)
        features = prepare_features(df)
        df["anomaly_score"] = model.decision_function(features)
        df["risk_score"] = df.apply(calculate_risk, axis=1)
        df["status"] = df["risk_score"].apply(
            lambda x: "High Risk" if x > 70 else "Medium Risk" if x > 40 else "Normal"
        )

        row = df.iloc[0]

        # Track failed attempts
        if row["login_status"] == "failure":
            ip_attempts[ip_address] += 1
        else:
            ip_attempts[ip_address] = 0  # reset on success

        # Save log to CSV
        try:
            # Reorder columns to match format if possible, or just dump
            # If we don't reload the file, we might overwrite? No, append mode.
            # But we need to use pandas to match schema or plain csv append.
            # Using pandas for consistency.
            log_df = df.copy()
            # Ensure timestamp is string for CSV
            log_df["timestamp"] = log_df["timestamp"].astype(str)
            
            # Load existing to concat? Excessive for one line.
            # Just append to file using mode='a' header=False?
            # But we must ensure columns match.
            # Safest is to read, concat, write if file is small (which it is for this demo).
            # For production, we'd use a database.
            try:
                existing_logs = pd.read_csv(app.config["DATA_PATH"])
                updated_logs = pd.concat([existing_logs, log_df], ignore_index=True)
            except FileNotFoundError:
                updated_logs = log_df
            
            updated_logs.to_csv(app.config["DATA_PATH"], index=False)
        except Exception as e:
            print(f"Error saving log: {e}")

        # Process blocking & alert
        if process_login_attempt(row):
            error = "⚠ Suspicious activity detected! Your IP has been blocked."
            return render_template("login.html", error=error)

        # Login result
        if app.config["USER_DB"].get(username) == password:
            return redirect("/dashboard")
        else:
            error = "Invalid credentials."

    return render_template("login.html", error=error)

@app.route("/dashboard")
def dashboard():
    try:
        df = pd.read_csv(app.config["DATA_PATH"])
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "user_id", "ip_address", "login_status", "device_type", "location", "risk_score", "status"])
    df = parse_logs(df)
    features = prepare_features(df)
    df["anomaly_score"] = model.decision_function(features)
    df["risk_score"] = df.apply(calculate_risk, axis=1)
    df["status"] = df["risk_score"].apply(
        lambda x: "High Risk" if x > 70 else "Medium Risk" if x > 40 else "Normal"
    )

    # Removed: process_login_attempt loop
    # We should only process logs when they happen (at login time), not when viewing dashboard.
    # Re-processing here would cause duplicate alerts/blocks for old events.

    return render_template(
        "dashboard.html",
        total=len(df),
        high=len(df[df["status"] == "High Risk"]),
        medium=len(df[df["status"] == "Medium Risk"]),
        normal=len(df[df["status"] == "Normal"]),
        logs=df.tail(20).iloc[::-1].to_dict(orient="records"), # Show newest first
        risk_chart=generate_risk_chart(df),
        hour_chart=generate_hour_chart(df)
    )

if __name__ == "__main__":
    app.run(debug=True)
