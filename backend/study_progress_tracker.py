from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64
from supabase_client import supabase

def log_study_session(date_input=None, hours=None, user_id=None):

    if user_id is None:
        return {
            "success": False,
            "message": "User authentication required."
        }

    if date_input is None or date_input == "":
        current_date = datetime.now().strftime("%Y-%m-%d")

    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            current_date = date_input

        except ValueError:
            return {
                "success": False,
                "message": "Invalid date format. Please use YYYY-MM-DD format."
            }

    if hours is None:
        return {
            "success": False,
            "message": "Hours studied is required."
        }

    try:
        hours = float(hours)

        if hours < 0:
            return {
                "success": False,
                "message": "Please enter a positive number."
            }

    except ValueError:
        return {
            "success": False,
            "message": "Invalid input. Please enter a numeric value."
        }

    try:

        response = (
            supabase
            .table("study_sessions")
            .insert({
                "user_id": user_id,
                "session_date": current_date,
                "hours_studied": hours
            })
            .execute()
        )

        return {
            "success": True,
            "message": f"Study session logged: {current_date}"
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


def load_logged_data(user_id):

    if user_id is None:
        return {}

    try:

        response = (
            supabase
            .table("study_sessions")
            .select("*")
            .eq("user_id", user_id)
            .order("session_date")
            .execute()
        )

        rows = response.data

        data = {}

        for row in rows:

            date = row["session_date"]

            hours = float(row["hours_studied"])

            data.setdefault(date, []).append(hours)

        return data

    except Exception as e:

        print("Error loading data:", e)

        return {}


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
