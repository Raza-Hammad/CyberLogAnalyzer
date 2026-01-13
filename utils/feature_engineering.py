from sklearn.preprocessing import LabelEncoder

# Fixed mappings based on typical usage to ensure consistency
# In a real scenario, these would be loaded from artifacts saved during training.
DEVICE_MAP = {"web": 0, "mobile": 1, "tablet": 2}
LOCATION_MAP = {"unknown": 0, "US": 1, "UK": 2, "CA": 3} # Example placeholders

def prepare_features(df):
    """
    Prepare features for the model.
    Note: In a production system, we would load the scaler/encoders used during training.
    Here we use manual mapping to ensure single-row inference works meaningfully
    compared to the 'always 0' bug of re-fitting LabelEncoder on single rows.
    """
    
    # Use map with fallback to 0 (unknown) to handle new values gracefully
    df["device_enc"] = df["device_type"].map(DEVICE_MAP).fillna(0).astype(int)
    # Simple hash-like fallback for location if not using a comprehensive map
    # or just map 'unknown' to 0 and others to their hash mod 100 for variety if map is small
    df["location_enc"] = df["location"].map(LOCATION_MAP).fillna(0).astype(int)

    features = df[
        ["hour", "is_night", "login_failed", "device_enc", "location_enc"]
    ]
    return features
