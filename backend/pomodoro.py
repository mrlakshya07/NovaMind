from datetime import datetime, timedelta

def start_pomodoro(minutes):
    """Start a pomodoro timer - web version"""
    try:
        minutes = int(minutes)
        if minutes <= 0:
            return {"success": False, "message": "Please enter a valid number of minutes."}
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=minutes)
        
        return {
            "success": True,
            "minutes": minutes,
            "start_time": start_time.strftime("%H:%M:%S"),
            "end_time": end_time.strftime("%H:%M:%S"),
            "total_seconds": minutes * 60
        }
    except (ValueError, TypeError):
        return {"success": False, "message": "Invalid input. Please enter a number."}

def get_remaining_time(end_time_str):
    """Calculate remaining time for active timer"""
    try:
        end_time = datetime.strptime(end_time_str, "%H:%M:%S")
        current_time = datetime.now()
        
        # Handle the case where timer crosses midnight
        if end_time < current_time:
            return 0
        
        remaining = (end_time - current_time).total_seconds()
        return max(0, int(remaining))
    except:
        return 0