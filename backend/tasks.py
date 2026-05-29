"""
Task management module for NovaMind.
Uses Supabase PostgreSQL for storage with user isolation.
Replaces txt-file based storage.
"""

from datetime import datetime
from supabase_client import supabase
from achievements import check_achievements


def load_tasks(user_id):
    """
    Load all tasks for a user from PostgreSQL.
    
    Args:
        user_id: UUID of authenticated user
        
    Returns:
        List of task dicts with id, title, status, created_at
    """
    if user_id is None:
        return []
    
    try:
        response = (
            supabase
            .table("tasks")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=False)
            .execute()
        )
        
        tasks = []
        for row in response.data:
            tasks.append({
                "id": row["id"],
                "title": row["task"],
                "completed": row["completed"],
                "priority": row.get("priority"),
                "due_date": row.get("due_date"),
                "created_at": row["created_at"]
            })
        return tasks
    
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return []


def add_task(task_text, user_id):
    """
    Add a new task for a user.
    
    Args:
        task_text: Task description
        user_id: UUID of authenticated user
        
    Returns:
        dict with success status and message
    """
    if user_id is None:
        return {"success": False, "message": "User authentication required."}
    
    if not task_text or not task_text.strip():
        return {"success": False, "message": "Task cannot be empty."}
    
    try:
        response = (
            supabase
            .table("tasks")
            .insert({
                "user_id": user_id,
                "task": task_text.strip(),
                "completed": False,
                "created_at": datetime.utcnow().isoformat()
            })
            .execute()
        )
        
        new_achievements = check_achievements(user_id)
        return {
            "success": True,
            "message": "Task added successfully.",
            "task_id": response.data[0]["id"] if response.data else None,
            "achievements": new_achievements
        }
    
    except Exception as e:
        return {"success": False, "message": f"Error adding task: {str(e)}"}


def toggle_task(task_id, user_id):
    """
    Toggle task status between 'todo' and 'done'.
    
    Args:
        task_id: UUID of task (from PostgreSQL)
        user_id: UUID of authenticated user
        
    Returns:
        dict with success status and message
    """
    if user_id is None:
        return {"success": False, "message": "User authentication required."}
    
    try:
        # Fetch current task
        response = (
            supabase
            .table("tasks")
            .select("completed")
            .eq("id", task_id)
            .eq("user_id", user_id)
            .single()
            .execute()
        )
        
        if not response.data:
            return {"success": False, "message": "Task not found."}
        
        current_status = response.data["completed"]
        new_status = not current_status
        
        # Update task status
        supabase.table("tasks").update({
            "completed": new_status
        }).eq("id", task_id).eq("user_id", user_id).execute()

        new_achievements = []

        if new_status:
            new_achievements = check_achievements(user_id)
        
        return {
            "success": True,
            "message": f"Task marked as {new_status}.",
            "achievements": new_achievements
        }
    
    except Exception as e:
        return {"success": False, "message": f"Error toggling task: {str(e)}"}


def delete_task(task_id, user_id):
    """
    Delete a task for a user.
    
    Args:
        task_id: UUID of task (from PostgreSQL)
        user_id: UUID of authenticated user
        
    Returns:
        dict with success status and message
    """
    if user_id is None:
        return {"success": False, "message": "User authentication required."}
    
    try:
        # Delete only user's task
        response = (
            supabase
            .table("tasks")
            .delete()
            .eq("id", task_id)
            .eq("user_id", user_id)
            .execute()
        )
        
        if not response.data or len(response.data) == 0:
            return {"success": False, "message": "Task not found."}
        
        return {"success": True, "message": "Task deleted successfully."}
    
    except Exception as e:
        return {"success": False, "message": f"Error deleting task: {str(e)}"}