"""
Pomodoro timer and session management for NovaMind.
Supports both real-time countdown and session persistence.
"""

from datetime import datetime, timedelta
from supabase_client import supabase
from achievements import check_achievements


def start_pomodoro(minutes):
    """
    Start a pomodoro timer - web version
    Returns timer details for frontend countdown
    """
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


def save_pomodoro_session(user_id, duration_minutes, focus_score=100):
    """
    Save a completed pomodoro session to the database.
    
    Args:
        user_id: UUID of authenticated user
        duration_minutes: Duration of the completed session
        focus_score: User's focus score for the session (default: 100)
    Returns:
        dict with success status and message
    """
    if user_id is None:
        return {"success": False, "message": "User authentication required."}
    
    try:
        duration_minutes = int(duration_minutes)
        if duration_minutes <= 0:
            return {"success": False, "message": "Invalid duration."}
        
        response = (
            supabase
            .table("pomodoro_sessions")
            .insert({
                "user_id": user_id,
                "focus_minutes": duration_minutes,
                "break_minutes": 5,
                "completed": True,
                "focus_score": focus_score
            })
            .execute()
        )

        new_achievements = check_achievements(user_id)
        return {
            "success": True,
            "message": f"Pomodoro session recorded: {duration_minutes} minutes",
            "achievements": new_achievements
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Error saving session: {str(e)}"
        }


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


def get_user_pomodoro_stats(user_id):
    """
    Get pomodoro statistics for a user.
    
    Args:
        user_id: UUID of authenticated user
        
    Returns:
        dict with stats (total_sessions, total_minutes, today_sessions)
    """
    if user_id is None:
        return {
            "total_sessions": 0,
            "total_minutes": 0,
            "today_sessions": 0,
            "today_minutes": 0
        }
    
    try:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        # Get all user pomodoro sessions
        response = (
            supabase
            .table("pomodoro_sessions")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        
        all_sessions = response.data or []
        total_sessions = len(all_sessions)
        total_minutes = sum(int(s["focus_minutes"]) for s in all_sessions)
        
        # Get today's sessions
        today_sessions = [
            s for s in all_sessions
            if s["created_at"][:10] == today
        ]
        today_count = len(today_sessions)
        today_minutes = sum(int(s["focus_minutes"]) for s in today_sessions)
        
        return {
            "total_sessions": total_sessions,
            "total_minutes": total_minutes,
            "today_sessions": today_count,
            "today_minutes": today_minutes
        }
    
    except Exception as e:
        print(f"Error getting pomodoro stats: {e}")
        return {
            "total_sessions": 0,
            "total_minutes": 0,
            "today_sessions": 0,
            "today_minutes": 0
        }
