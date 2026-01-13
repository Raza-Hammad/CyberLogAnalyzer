import os

class Config:
    """Project configuration settings."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    
    # Paths (Relative to project root)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "data/login_logs.csv")
    MODEL_PATH = os.path.join(BASE_DIR, "ml/anomaly_model.pkl")
    BLOCK_FILE = os.path.join(BASE_DIR, "data/blocked_ips.csv")
    
    # Simulated User Database
    USER_DB = {
        "admin": "admin123",
        "user1": "pass1",
        "analyst": "securePass!"
    }

    # Application Settings
    DEBUG = True
    MAX_LOGIN_ATTEMPTS = 3
    BLOCK_THRESHOLD_HIGH = 85
    BLOCK_THRESHOLD_MEDIUM = 70
