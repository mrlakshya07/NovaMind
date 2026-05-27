import os
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

BASE_DIR = os.path.dirname(__file__)
STUDY_LOG_FILE = os.path.join(BASE_DIR, "study_log.txt")

def log_study_session(date_input=None, hours=None):
    if date_input is None or date_input == "":
        current_date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            current_date = date_input
        except ValueError:
            return {"success": False, "message": "Invalid date format. Please use YYYY-MM-DD format."}

    if hours is None:
        return {"success": False, "message": "Hours studied is required."}

    try:
        hours = float(hours)
        if hours < 0:
            return {"success": False, "message": "Please enter a positive number."}
    except ValueError:
        return {"success": False, "message": "Invalid input. Please enter a numeric value."}

    with open(STUDY_LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{current_date},{hours}\n")
    return {"success": True, "message": f"Study session logged: {current_date}, {hours} hours"}


def load_logged_data():
    data = {}
    try:
        with open(STUDY_LOG_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    date, hour = parts[0], float(parts[1])
                    data.setdefault(date, []).append(hour)
    except FileNotFoundError:
        return {}
    return data


def show_all_history(data):
    if not data:
        return "No data available."
    history = "Study Data History:\n"
    for date in sorted(data):
        hours_list = data[date]
        history += f"{date}: {', '.join(map(str, hours_list))} hours\n"
    return history


def plot_average_study_time(data):
    if not data:
        return None
    dates = sorted(data)
    avg_hours = [sum(hours) / len(hours) for hours in (data[date] for date in dates)]

    plt.figure(figsize=(9, 5))
    plt.bar(dates, avg_hours, color="#2F167A")
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Average Hours Studied', fontweight='bold')
    plt.title('Average Study Time per Day', fontweight='bold')
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url
