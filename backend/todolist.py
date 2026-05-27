from datetime import datetime

def addtasks():
    task = input("Enter your task: ").strip()
    if not task:
        print("Empty task cannot be added.")
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("tasks.txt", "a") as f:
        f.write(f"[ ] {task} (added: {timestamp})\n")
    print("Task added!")

def view_tasks():
    try:
        with open("tasks.txt", "r") as f:
            tasks = f.readlines()
        if not tasks:
            print("No tasks added!")
        else:
            print("\nYour Tasks:")
            for idx, t in enumerate(tasks, start=1):
                print(f"{idx}. {t.strip()}")
    except FileNotFoundError:
        print("No tasks yet!")

def markdone_unmark():
    try:
        with open("tasks.txt", "r") as f:
            tasks = f.readlines()
        if not tasks:
            print("No tasks to update.")
            return
        view_tasks()
        taskno = int(input("Enter task number to toggle done status: "))
        if 1 <= taskno <= len(tasks):
            task_line = tasks[taskno - 1]
            if "[ ]" in task_line:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                task_line = task_line.replace("[ ]", f"[done at {timestamp}]")
            elif "[done" in task_line:
                task_line = task_line.replace(task_line[:task_line.index("]")+1], "[ ]")
            else:
                print("Task status unrecognized.")
                return
            tasks[taskno - 1] = task_line
            with open("tasks.txt", "w") as f:
                f.writelines(tasks)
            print("Task status toggled!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")
    except FileNotFoundError:
        print("No tasks found.")

def deletetask():
    try:
        with open("tasks.txt", "r") as f:
            tasks = f.readlines()
        if not tasks:
            print("No tasks to delete.")
            return
        view_tasks()
        taskno = int(input("Enter task number to delete: "))
        if 1 <= taskno <= len(tasks):
            removed = tasks.pop(taskno - 1)
            with open("tasks.txt", "w") as f:
                f.writelines(tasks)
            print(f"Deleted task: {removed.strip()}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")
    except FileNotFoundError:
        print("No tasks found.")

def searchtasks():
    keyword = input("Enter keyword to search: ").strip().lower()
    if not keyword:
        print("Empty keyword, please enter something.")
        return
    try:
        with open("tasks.txt", "r") as f:
            tasks = f.readlines()
    except FileNotFoundError:
        print("No tasks found.")
        return
    results = [(idx+1, t.strip()) for idx, t in enumerate(tasks) if keyword in t.lower()]
    if not results:
        print(f"No tasks found containing '{keyword}'.")
    else:
        print(f"\nTasks containing '{keyword}':")
        for num, task in results:
            print(f"{num}. {task}")

def task_choice():
    while True:
        print("\n\t\t----To Do List----")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Toggle Task Done/Undone")
        print("4. Delete Task")
        print("5. Search Tasks")
        print("6. Exit")
        ch = input("Enter your choice: ").strip()
        match ch:
            case "1":
                addtasks()
            case "2":
                view_tasks()
            case "3":
                markdone_unmark()
            case "4":
                deletetask()
            case "5":
                searchtasks()
            case "6":
                print("Goodbye!")
                break
            case _:
                print("Invalid choice, please enter 1 to 6.")

task_choice()