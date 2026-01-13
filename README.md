# Cyber Log Analyzer

Cyber Log Analyzer is a robust machine learning–based security system designed to detect suspicious login behavior in real-time. It assigns risk scores to login attempts, automatically blocks malicious IP addresses, and provides a comprehensive admin dashboard for security monitoring.

## 🚀 Features

- **Real-time Risk Scoring:** Analyzes login attempts and assigns a risk score based on various features.
- **Automated IP Blocking:** Automatically blocks IP addresses that exceed a defined risk threshold.
- **Admin Dashboard:** Visualizes security data, including risk distribution and login activity over time.
- **Anomaly Detection:** Uses a trained Machine Learning model to identify deviations from normal user behavior.
- **Alerting System:** Triggers alerts for high-risk activities (configured in `utils/alerts.py`).

## 🛠️ Technologies Used

- **Python 3.x**
- **Flask:** Web framework for the application interface.
- **Pandas:** Data manipulation and log analysis.
- **Scikit-learn:** Machine learning model for anomaly detection.
- **Joblib:** Model persistence.
- **Matplotlib:** Data visualization for the dashboard.
- **HTML/CSS/JS:** Frontend for the login page and dashboard.

## 📂 Project Structure

```
CyberLogAnalyzer/
├── app.py                  # Main Flask application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── data/                   # Directory for storing logs and block lists
├── ml/                     # Machine Learning resources (models, training scripts)
├── static/                 # Static assets (CSS, JS, images)
├── templates/              # HTML templates
└── utils/                  # Utility modules
    ├── alerts.py           # Alerting logic
    ├── feature_engineering.py # Feature extraction for ML
    ├── ip_blocker.py       # IP blocking mechanisms
    ├── log_parser.py       # Log parsing utilities
    ├── risk_scoring.py     # Risk calculation logic
    └── visualization.py    # Chart generation
```

## ⚡ Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd CyberLogAnalyzer
    ```

2.  **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃 Usage

1.  **Start the application:**
    ```bash
    python app.py
    ```

2.  **Access the application:**
    -   **Login Page:** Open your browser and navigate to `http://127.0.0.1:5000/`.
    -   **Admin Dashboard:** Navigate to `http://127.0.0.1:5000/dashboard`.

## 🛡️ Security Logic

-   **Normal (Risk Score <= 40):** Access granted.
-   **Medium Risk (40 < Risk Score <= 70):** Monitored; blocked after 1 failed attempt.
-   **High Risk (Risk Score > 70):** Immediate block and alert triggered.
-   **Extreme Risk (Risk Score > 85):** Immediate block and alert.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
