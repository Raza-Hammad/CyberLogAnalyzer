import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import sys
import os

# Add project root to path so utils can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.log_parser import parse_logs
from utils.feature_engineering import prepare_features

# Correct path to your CSV file
df = pd.read_csv(r"C:\Users\stc\Desktop\CyberLogAnalyzer\data\login_logs.csv")

# Parse logs and prepare features
df = parse_logs(df)
X = prepare_features(df)

# Train the Isolation Forest model
model = IsolationForest(
    n_estimators=100,
    contamination=0.1,
    random_state=42
)

model.fit(X)

# Save the trained model
joblib.dump(model, "ml/anomaly_model.pkl")

print("Model trained and saved.")
