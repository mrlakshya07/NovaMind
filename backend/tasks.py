import os
from datetime import datetime

BASE_DIR = os.path.dirname(__file__)
TASKS_FILE = os.path.join(BASE_DIR, "tasks.txt")

def load_tasks():
    tasks = []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f.readlines(), start=1):
                line = line.strip()
                if not line:
                    continue
                status = "todo"
                if line.startswith("[done"):
                    status = "done"
                tasks.append({"id": idx, "raw": line, "status": status})
    except FileNotFoundError:
        return []
    return tasks


def add_task(task_text):
    if not task_text or not task_text.strip():
        return {"success": False, "message": "Task cannot be empty."}

    with open(TASKS_FILE, "a", encoding="utf-8") as f:
        f.write(f"[ ] {task_text.strip()}\n")
    return {"success": True, "message": "Task added successfully."}


def toggle_task(task_index):
    try:
        task_index = int(task_index)
    except (TypeError, ValueError):
        return {"success": False, "message": "Invalid task index."}

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = [line.rstrip("\n") for line in f.readlines()]
    except FileNotFoundError:
        return {"success": False, "message": "No tasks available."}

    if task_index < 1 or task_index > len(tasks):
        return {"success": False, "message": "Task index out of range."}

    current = tasks[task_index - 1]
    if current.startswith("[ ]"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tasks[task_index - 1] = current.replace("[ ]", f"[done at {timestamp}]", 1)
    elif current.startswith("[done"):
        rest = current[current.index("]") + 1:].strip()
        tasks[task_index - 1] = f"[ ] {rest}"
    else:
        return {"success": False, "message": "Task status is not recognized."}

    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(tasks) + ("\n" if tasks else ""))

    return {"success": True, "message": "Task status updated."}


def delete_task(task_index):
    try:
        task_index = int(task_index)
    except (TypeError, ValueError):
        return {"success": False, "message": "Invalid task index."}

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = [line.rstrip("\n") for line in f.readlines()]
    except FileNotFoundError:
        return {"success": False, "message": "No tasks found."}

    if task_index < 1 or task_index > len(tasks):
        return {"success": False, "message": "Task index out of range."}

    removed = tasks.pop(task_index - 1)
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(tasks) + ("\n" if tasks else ""))

    return {"success": True, "message": f"Deleted task: {removed}"}
