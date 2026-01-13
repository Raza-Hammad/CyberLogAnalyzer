import matplotlib
matplotlib.use('Agg') # Non-GUI backend
import matplotlib.pyplot as plt
import io
import base64

def get_base64_image():
    """Helper to convert current plot to base64 string"""
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return "data:image/png;base64," + base64.b64encode(img.getvalue()).decode()

def generate_risk_chart(df):
    """Generate a pie chart for risk distribution"""
    plt.figure(figsize=(6, 4))
    
    # Check if 'status' exists, if empty default to something
    if df.empty or "status" not in df.columns:
        plt.text(0.5, 0.5, "No Data", ha='center')
        return get_base64_image()

    counts = df["status"].value_counts()
    if counts.empty:
        plt.text(0.5, 0.5, "No Data", ha='center')
        return get_base64_image()
        
    colors = {'High Risk': '#dc3545', 'Medium Risk': '#ffc107', 'Normal': '#28a745'}
    # Map colors to index
    plot_colors = [colors.get(x, '#6c757d') for x in counts.index]
    
    counts.plot(kind='pie', autopct='%1.1f%%', colors=plot_colors, startangle=90)
    plt.title("Risk Distribution")
    plt.ylabel("") # Hide y-label
    
    img_str = get_base64_image()
    plt.close()
    return img_str

def generate_hour_chart(df):
    """Generate a bar chart for logins per hour"""
    plt.figure(figsize=(6, 4))
    
    if df.empty or "hour" not in df.columns:
        plt.text(0.5, 0.5, "No Data", ha='center')
        return get_base64_image()

    counts = df["hour"].value_counts().sort_index()
    counts.plot(kind='bar', color='#007bff')
    plt.title("Logins per Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Count")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    img_str = get_base64_image()
    plt.close()
    return img_str
