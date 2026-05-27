import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
NOTES_FILE = os.path.join(BASE_DIR, "notes.txt")

def addnotes(note_text):
    if not note_text or not note_text.strip():
        return {"success": False, "message": "Empty note not saved."}

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {note_text}\n")
        return {"success": True, "message": "Note saved with timestamp!"}
    except IOError:
        return {"success": False, "message": "Error: Could not write to notes.txt"}


def viewnotes():
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes = f.readlines()
        return [n.strip() for n in notes if n.strip()]
    except FileNotFoundError:
        return []
    except IOError:
        return []


def deletenotes(note_number):
    notes = viewnotes()
    if not notes:
        return {"success": False, "message": "No notes found."}

    try:
        if note_number < 1 or note_number > len(notes):
            return {"success": False, "message": "Invalid note number."}

        removed_note = notes.pop(note_number - 1)
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            f.writelines([note + "\n" for note in notes])

        return {"success": True, "message": f"Deleted note: {removed_note}"}
    except ValueError:
        return {"success": False, "message": "Please enter a valid number."}
    except IOError:
        return {"success": False, "message": "Error: Could not update notes.txt"}


def searchnotes(keyword):
    if not keyword or not keyword.strip():
        return {"success": False, "message": "Empty keyword, please enter something to search.", "results": []}

    keyword = keyword.strip().lower()
    notes = viewnotes()
    if not notes:
        return {"success": False, "message": "No notes found.", "results": []}

    results = [(idx + 1, note) for idx, note in enumerate(notes) if keyword in note.lower()]
    if not results:
        return {"success": False, "message": f"No notes found containing '{keyword}'.", "results": []}
    return {"success": True, "message": f"Found {len(results)} note(s) containing '{keyword}'", "results": results}
