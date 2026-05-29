"""
Achievement system for NovaMind.
Tracks and awards achievements based on user milestones and actions.
Provides a unified check_achievements() service called by all action modules.
"""

from datetime import datetime, date, timedelta
from supabase_client import supabase


# Achievement definitions organized by category
ACHIEVEMENTS = {
    # Study Achievements
    "first_session": {
        "name": "First Session",
        "description": "Log your first study session",
        "icon": "🌱",
        "category": "Study Achievements",
        "rarity": "common",
        "xp":50
    },
    "ten_study_hours": {
        "name": "Study Apprentice",
        "description": "Reach 10 study hours",
        "icon": "📚",
        "category": "Study Achievements",
        "rarity": "uncommon",
        "xp":100
    },
    "fifty_study_hours": {
        "name": "Knowledge Builder",
        "description": "Reach 50 study hours",
        "icon": "🎓",
        "category": "Study Achievements",
        "rarity": "rare",
        "xp":250
    },
    "hundred_study_hours": {
        "name": "Study Master",
        "description": "Reach 100 study hours",
        "icon": "🏆",
        "category": "Study Achievements",
        "rarity": "epic",
        "xp":500
    },
    
    # Note Achievements
    "first_note": {
        "name": "First Note",
        "description": "Create your first note",
        "icon": "📝",
        "category": "Note Achievements",
        "rarity": "common",
        "xp":50
    },
    "ten_notes": {
        "name": "Note Taker",
        "description": "Create 10 notes",
        "icon": "📒",
        "category": "Note Achievements",
        "rarity": "uncommon",
        "xp":100
    },
    "hundred_notes": {
        "name": "Knowledge Scribe",
        "description": "Create 100 notes",
        "icon": "📖",
        "category": "Note Achievements",
        "rarity": "rare",
        "xp":250
    },
    
    # Task Achievements
    "first_task": {
        "name": "First Task",
        "description": "Create your first task",
        "icon": "✅",
        "category": "Task Achievements",
        "rarity": "common",
        "xp":50
    },
    "first_task_completed": {
        "name": "Task Starter",
        "description": "Complete your first task",
        "icon": "🎯",
        "category": "Task Achievements",
        "rarity": "common",
        "xp":50
    },
    "ten_tasks_completed": {
        "name": "Productivity Starter",
        "description": "Complete 10 tasks",
        "icon": "⚡",
        "category": "Task Achievements",
        "rarity": "uncommon",
        "xp":100
    },
    "fifty_tasks_completed": {
        "name": "Task Champion",
        "description": "Complete 50 tasks",
        "icon": "🚀",
        "category": "Task Achievements",
        "rarity": "epic",
        "xp":500
    },
    
    # Focus Achievements
    "first_pomodoro": {
        "name": "First Focus Session",
        "description": "Complete your first Pomodoro",
        "icon": "⏳",
        "category": "Focus Achievements",
        "rarity": "common",
        "xp":50
    },
    "twenty_five_pomodoros": {
        "name": "Focus Builder",
        "description": "Complete 25 Pomodoro sessions",
        "icon": "🎯",
        "category": "Focus Achievements",
        "rarity": "uncommon",
        "xp":100
    },
    "hundred_pomodoros": {
        "name": "Deep Work Master",
        "description": "Complete 100 Pomodoro sessions",
        "icon": "🔥",
        "category": "Focus Achievements",
        "rarity": "epic",
        "xp":500
    },
    "focus_perfectionist": {
        "name": "Focus Perfectionist",
        "description": "Complete a session with 95%+ focus score",
        "icon": "💎",
        "category": "Focus Achievements",
        "rarity": "rare",
        "xp":250
    },
    
    # Consistency Achievements
    "three_day_streak": {
        "name": "3 Day Streak",
        "description": "Maintain a 3-day study streak",
        "icon": "📅",
        "category": "Consistency Achievements",
        "rarity": "uncommon",
        "xp":100
    },
    "seven_day_streak": {
        "name": "7 Day Streak",
        "description": "Maintain a 7-day study streak",
        "icon": "🔥",
        "category": "Consistency Achievements",
        "rarity": "rare",
        "xp":250
    },
    "thirty_day_streak": {
        "name": "30 Day Streak",
        "description": "Maintain a 30-day study streak",
        "icon": "🚀",
        "category": "Consistency Achievements",
        "rarity": "epic",
        "xp":500
    },
    "consistency_legend": {
        "name": "Consistency Legend",
        "description": "Maintain a 100-day study streak",
        "icon": "👑",
        "category": "Consistency Achievements",
        "rarity": "legendary",
        "xp":1000
    }
}


def check_achievements(user_id):
    """
    Unified achievement checking service.
    Checks ALL achievement categories for a user and awards any newly earned.
    
    This is the primary function that should be called from:
    - tasks.py (on add/toggle)
    - notes.py (on add)
    - pomodoro.py (on session complete)
    - study_progress_tracker.py (on session log)
    
    Args:
        user_id: UUID of authenticated user
        
    Returns:
        List of newly earned achievement dicts with name, description, icon, rarity, type
    """
    if user_id is None:
        return []
    
    newly_earned = []
    
    try:
        # Get all currently earned achievement types for this user
        existing = _get_earned_types(user_id)
        
        # Check all categories
        candidates = []
        candidates.extend(_check_note_achievements(user_id))
        candidates.extend(_check_task_achievements(user_id))
        candidates.extend(_check_session_achievements(user_id))
        candidates.extend(_check_pomodoro_achievements(user_id))
        candidates.extend(_check_streak_achievements(user_id))
        
        # Award only truly new achievements
        for achievement_type in candidates:
            if achievement_type not in existing:
                if _award_achievement(user_id, achievement_type):
                    if achievement_type in ACHIEVEMENTS:
                        achievement_data = ACHIEVEMENTS[achievement_type]
                        newly_earned.append({
                            "type": achievement_type,
                            "name": achievement_data["name"],
                            "description": achievement_data["description"],
                            "icon": achievement_data["icon"],
                            "rarity": achievement_data.get("rarity", "common"),
                            "xp": achievement_data.get("xp", 0)
                        })
    
    except Exception as e:
        print(f"Error in check_achievements: {e}")
    
    return newly_earned


def _get_earned_types(user_id):
    """Get set of achievement types already earned by user."""
    try:
        response = (
            supabase
            .table("achievements")
            .select("type")
            .eq("user_id", user_id)
            .execute()
        )
        return {row["type"] for row in (response.data or [])}
    except Exception as e:
        print(f"Error getting earned types: {e}")
        return set()


def _check_note_achievements(user_id):
    """Check note-related achievements."""
    earned = []
    
    try:
        response = supabase.table("notes").select("id").eq("user_id", user_id).execute()
        count = len(response.data) if response.data else 0
        
        if count >= 1:
            earned.append("first_note")
        if count >= 10:
            earned.append("ten_notes")
        if count >= 100:
            earned.append("hundred_notes")
    
    except Exception as e:
        print(f"Error checking note achievements: {e}")
    
    return earned


def _get_total_study_hours(user_id):
    """Get total study hours for user from study_sessions."""
    try:
        response = supabase.table("study_sessions").select("hours_studied").eq("user_id", user_id).execute()
        if response.data:
            total_hours = sum(float(session.get("hours_studied", 0)) for session in response.data)
            return total_hours
        return 0
    except Exception as e:
        print(f"Error getting study hours: {e}")
        return 0


def _check_task_achievements(user_id):
    """Check task-related achievements."""
    earned = []
    
    try:
        # Count total tasks created
        all_tasks = supabase.table("tasks").select("id").eq("user_id", user_id).execute()
        total_count = len(all_tasks.data) if all_tasks.data else 0
        
        if total_count >= 1:
            earned.append("first_task")
        
        # Count completed tasks
        done_tasks = supabase.table("tasks").select("id").eq("user_id", user_id).eq("completed", True).execute()
        done_count = len(done_tasks.data) if done_tasks.data else 0
        
        if done_count >= 1:
            earned.append("first_task_completed")
        if done_count >= 10:
            earned.append("ten_tasks_completed")
        if done_count >= 50:
            earned.append("fifty_tasks_completed")
    
    except Exception as e:
        print(f"Error checking task achievements: {e}")
    
    return earned


def _check_session_achievements(user_id):
    """Check study session achievements."""
    earned = []
    
    try:
        response = supabase.table("study_sessions").select("id").eq("user_id", user_id).execute()
        count = len(response.data) if response.data else 0
        
        if count >= 1:
            earned.append("first_session")
        
        # Check study hours milestones
        total_hours = _get_total_study_hours(user_id)
        
        if total_hours >= 10:
            earned.append("ten_study_hours")
        if total_hours >= 50:
            earned.append("fifty_study_hours")
        if total_hours >= 100:
            earned.append("hundred_study_hours")
    
    except Exception as e:
        print(f"Error checking session achievements: {e}")
    
    return earned


def _check_pomodoro_achievements(user_id):
    """Check pomodoro-related achievements."""
    earned = []
    
    try:
        response = supabase.table("pomodoro_sessions").select("id").eq("user_id", user_id).execute()
        sessions = response.data or []
        count = len(sessions)
        
        if count >= 1:
            earned.append("first_pomodoro")
        if count >= 25:
            earned.append("twenty_five_pomodoros")
        if count >= 100:
            earned.append("hundred_pomodoros")
        focus_response = (
            supabase
            .table("pomodoro_sessions")
            .select("focus_score, focus_minutes")
            .eq("user_id", user_id)
            .gte("focus_score", 95)
            .gte("focus_minutes", 25)
            .limit(1)
            .execute()
        )

        if focus_response.data:
            earned.append("focus_perfectionist")
    
    except Exception as e:
        print(f"Error checking pomodoro achievements: {e}")
    
    return earned


def _check_streak_achievements(user_id):
    """Check streak-based achievements by computing current streak."""
    earned = []
    
    try:
        streak = _compute_current_streak(user_id)
        
        if streak >= 3:
            earned.append("three_day_streak")
        if streak >= 7:
            earned.append("seven_day_streak")
        if streak >= 30:
            earned.append("thirty_day_streak")
        if streak >= 100:
            earned.append("consistency_legend")
    
    except Exception as e:
        print(f"Error checking streak achievements: {e}")
    
    return earned


def _compute_current_streak(user_id):
    """Compute the current study streak (consecutive days with activity)."""
    try:
        # Get unique study dates from study_sessions
        study_response = (
            supabase
            .table("study_sessions")
            .select("session_date")
            .eq("user_id", user_id)
            .execute()
        )
        study_dates = set()
        for row in (study_response.data or []):
            try:
                study_dates.add(row["session_date"])
            except (KeyError, ValueError):
                pass
        
        # Get unique dates from pomodoro_sessions
        pomo_response = (
            supabase
            .table("pomodoro_sessions")
            .select("created_at")
            .eq("user_id", user_id)
            .execute()
        )
        for row in (pomo_response.data or []):
            try:
                dt_str = row["created_at"][:10]  # Extract YYYY-MM-DD
                study_dates.add(dt_str)
            except (KeyError, ValueError, TypeError):
                pass
        
        if not study_dates:
            return 0
        
        # Parse and sort dates
        parsed_dates = sorted([
            datetime.strptime(d, "%Y-%m-%d").date() 
            for d in study_dates 
            if d
        ], reverse=True)
        
        if not parsed_dates:
            return 0
        
        # Walk backwards from today
        today = date.today()
        
        # If most recent activity isn't today or yesterday, streak is 0
        if parsed_dates[0] < today - timedelta(days=1):
            return 0
        
        streak = 1
        for i in range(1, len(parsed_dates)):
            expected = parsed_dates[i - 1] - timedelta(days=1)
            if parsed_dates[i] == expected:
                streak += 1
            elif parsed_dates[i] < expected:
                break
        
        return streak
    
    except Exception as e:
        print(f"Error computing streak: {e}")
        return 0


def _has_achievement(user_id, achievement_type):
    """Check if user already has an achievement."""
    try:
        response = (
            supabase
            .table("achievements")
            .select("id")
            .eq("user_id", user_id)
            .eq("type", achievement_type)
            .limit(1)
            .execute()
        )
        return bool(response.data)
    except:
        return False


def _award_achievement(user_id, achievement_type):
    """Award an achievement to a user. Returns True if successfully awarded."""
    try:
        achievement_data = ACHIEVEMENTS.get(achievement_type, {})

        supabase.table("achievements").insert({
            "user_id": user_id,
            "type": achievement_type,
            "badge_name": achievement_data.get("name"),
            "description": achievement_data.get("description"),
            "earned_at": datetime.utcnow().isoformat()
        }).execute()
        return True
    except Exception as e:
        # Duplicate constraint will cause this to fail silently
        error_str = str(e).lower()
        if "duplicate" in error_str or "unique" in error_str or "conflict" in error_str:
            return False
        print(f"Error awarding achievement '{achievement_type}': {e}")
        return False


def get_user_achievements(user_id):
    """
    Get all achievements earned by a user.
    
    Args:
        user_id: UUID of authenticated user
        
    Returns:
        List of achievement dicts with name, description, icon, earned_at
    """
    if user_id is None:
        return []
    
    try:
        response = (
            supabase
            .table("achievements")
            .select("*")
            .eq("user_id", user_id)
            .order("earned_at", desc=True)
            .execute()
        )
        
        user_achievements = []
        for row in response.data:
            achievement_type = row["type"]
            if achievement_type in ACHIEVEMENTS:
                achievement_data = ACHIEVEMENTS[achievement_type]
                user_achievements.append({
                    "type": achievement_type,
                    "name": achievement_data["name"],
                    "description": achievement_data["description"],
                    "icon": achievement_data["icon"],
                    "rarity": achievement_data.get("rarity", "common"),
                    "category": achievement_data.get("category", "Other"),
                    "xp": achievement_data.get("xp", 0),
                    "earned_at": row["earned_at"]
                })
        
        return user_achievements
    
    except Exception as e:
        print(f"Error getting achievements: {e}")
        return []


def get_achievement_progress(user_id):
    """
    Get progress toward next achievements.
    
    Args:
        user_id: UUID of authenticated user
        
    Returns:
        dict with progress toward next achievements
    """
    if user_id is None:
        return {}
    
    try:
        progress = {}
        
        # Study sessions progress
        sessions_response = supabase.table("study_sessions").select("id").eq("user_id", user_id).execute()
        sessions_count = len(sessions_response.data) if sessions_response.data else 0
        progress["sessions"] = {
            "current": sessions_count,
            "targets": [1]
        }
        
        # Study hours progress
        study_hours = _get_total_study_hours(user_id)
        progress["study_hours"] = {
            "current": round(study_hours, 1),
            "targets": [10, 50, 100]
        }
        
        # Notes progress
        notes_response = supabase.table("notes").select("id").eq("user_id", user_id).execute()
        notes_count = len(notes_response.data) if notes_response.data else 0
        progress["notes"] = {
            "current": notes_count,
            "targets": [1, 10, 100]
        }
        
        # Tasks progress
        tasks_response = supabase.table("tasks").select("id").eq("user_id", user_id).eq("completed", True).execute()
        tasks_count = len(tasks_response.data) if tasks_response.data else 0
        progress["tasks"] = {
            "current": tasks_count,
            "targets": [1, 10, 50]
        }
        
        # Pomodoros progress
        pomodoros_response = supabase.table("pomodoro_sessions").select("id").eq("user_id", user_id).execute()
        pomodoros_count = len(pomodoros_response.data) if pomodoros_response.data else 0
        progress["pomodoros"] = {
            "current": pomodoros_count,
            "targets": [1, 25, 100]
        }
        
        # Streak progress
        streak = _compute_current_streak(user_id)
        progress["streak"] = {
            "current": streak,
            "targets": [3, 7, 30, 100]
        }
        
        return progress
    
    except Exception as e:
        print(f"Error getting achievement progress: {e}")
        return {}


def get_achievement_stats(user_id):
    """
    Get achievement statistics for user dashboard.
    
    Args:
        user_id: UUID of authenticated user
        
    Returns:
        dict with achievement statistics
    """
    if user_id is None:
        return {}
    
    try:
        # Get all achievements
        response = (
            supabase
            .table("achievements")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        earned_achievements = response.data if response.data else []
        earned_types = {a["type"] for a in earned_achievements}
        total_xp = 0

        for achievement_type in earned_types:
            if achievement_type in ACHIEVEMENTS:
                total_xp += ACHIEVEMENTS[achievement_type].get("xp", 0)
        
        # Calculate stats
        total_achievements = len(ACHIEVEMENTS)
        unlocked_count = len(earned_types)
        completion_percentage = round((unlocked_count / total_achievements * 100)) if total_achievements > 0 else 0
        
        # Count by category
        categories = {}
        for ach_id, ach_data in ACHIEVEMENTS.items():
            category = ach_data.get("category", "Other")
            if category not in categories:
                categories[category] = {"total": 0, "unlocked": 0}
            categories[category]["total"] += 1
            if ach_id in earned_types:
                categories[category]["unlocked"] += 1
        
        return {
            "total": total_achievements,
            "unlocked": unlocked_count,
            "completion_percentage": completion_percentage,
            "total_xp": total_xp,
            "categories": categories
        }
    
    except Exception as e:
        print(f"Error getting achievement stats: {e}")
        return {
            "total": len(ACHIEVEMENTS),
            "unlocked": 0,
            "completion_percentage": 0,
            "categories": {}
        }