import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure your email
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Use App Password for Gmail
RECEIVER_EMAIL = "admin_email@gmail.com"

def send_alert(log):
    subject = f"⚠ High Risk Login Detected: {log['ip_address']}"
    body = f"""
    High Risk Login Detected!
    
    User: {log['user_id']}
    IP: {log['ip_address']}
    Device: {log['device_type']}
    Location: {log['location']}
    Time: {log['timestamp']}
    Risk Score: {log['risk_score']}
    Status: {log['status']}
    """
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    if "your_email" in SENDER_EMAIL or "your_app_password" in SENDER_PASSWORD:
        print(f"[Simulated Alert] Would send email to {RECEIVER_EMAIL} about {log['ip_address']}")
        return

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Alert sent for IP: {log['ip_address']}")
    except Exception as e:
        print("Failed to send alert:", e)
