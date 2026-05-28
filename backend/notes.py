"""
Notes management module for NovaMind.
Uses Supabase PostgreSQL for storage with user isolation.
Replaces txt-file based storage.
"""

from datetime import datetime
from supabase_client import supabase


def viewnotes(user_id):
    """
    View all notes for a user.
    
    Args:
        user_id: UUID of authenticated user
        
    Returns:
        List of note strings formatted as "[timestamp] content"
    """
    if user_id is None:
        return []
    
    try:
        response = (
            supabase
            .table("notes")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        
        notes = []
        for row in response.data:
            timestamp = row["created_at"][:19].replace("T", " ")  # Format: "2024-01-01 12:00:00"
            notes.append(f"[{timestamp}] {row['content']}")
        
        return notes
    
    except Exception as e:
        print(f"Error viewing notes: {e}")
        return []


def addnotes(note_text, user_id):
    """
    Add a new note for a user.
    
    Args:
        note_text: Note content
        user_id: UUID of authenticated user
        
    Returns:
        dict with success status and message
    """
    if user_id is None:
        return {"success": False, "message": "User authentication required."}
    
    if not note_text or not note_text.strip():
        return {"success": False, "message": "Empty note not saved."}
    
    try:
        timestamp = datetime.utcnow().isoformat()
        response = (
            supabase
            .table("notes")
            .insert({
                "user_id": user_id,
                "content": note_text.strip(),
                "created_at": timestamp
            })
            .execute()
        )
        
        return {
            "success": True,
            "message": "Note saved with timestamp!"
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }


def deletenotes(note_index, user_id):
    """
    Delete a note for a user by index.
    
    Args:
        note_index: 1-based index from viewnotes() list
        user_id: UUID of authenticated user
        
    Returns:
        dict with success status and message
    """
    if user_id is None:
        return {"success": False, "message": "User authentication required."}
    
    notes_list = viewnotes(user_id)
    
    if not notes_list:
        return {"success": False, "message": "No notes found."}
    
    try:
        note_index = int(note_index)
        if note_index < 1 or note_index > len(notes_list):
            return {"success": False, "message": "Invalid note number."}
        
        # Get all notes ordered by created_at descending
        response = (
            supabase
            .table("notes")
            .select("id")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        
        if not response.data or len(response.data) < note_index:
            return {"success": False, "message": "Invalid note number."}
        
        note_id = response.data[note_index - 1]["id"]
        
        # Delete by ID
        supabase.table("notes").delete().eq("id", note_id).eq("user_id", user_id).execute()
        
        return {
            "success": True,
            "message": f"Deleted note: {notes_list[note_index - 1]}"
        }
    
    except ValueError:
        return {"success": False, "message": "Please enter a valid number."}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def searchnotes(keyword, user_id):
    """
    Search notes for a user by keyword.
    
    Args:
        keyword: Search term
        user_id: UUID of authenticated user
        
    Returns:
        dict with search results and message
    """
    if user_id is None:
        return {
            "success": False,
            "message": "User authentication required.",
            "results": []
        }
    
    if not keyword or not keyword.strip():
        return {
            "success": False,
            "message": "Empty keyword, please enter something to search.",
            "results": []
        }
    
    keyword = keyword.strip().lower()
    notes = viewnotes(user_id)
    
    if not notes:
        return {
            "success": False,
            "message": "No notes found.",
            "results": []
        }
    
    results = [
        (idx + 1, note) 
        for idx, note in enumerate(notes) 
        if keyword in note.lower()
    ]
    
    if not results:
        return {
            "success": False,
            "message": f"No notes found containing '{keyword}'.",
            "results": []
        }
    
    return {
        "success": True,
        "message": f"Found {len(results)} note(s) containing '{keyword}'",
        "results": results
    }