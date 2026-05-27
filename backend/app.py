import os
import sys
from flask import Flask, request, jsonify, render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import notes
import study_progress_tracker as progress
import pomodoro
import tasks as task_module

FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

TEMPLATE_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes')
def notes_page():
    return render_template('notes.html')

@app.route('/tasks')
def tasks_page():
    return render_template('tasks.html')

@app.route('/pomodoro')
def pomodoro_page():
    return render_template('pomodoro.html')

@app.route('/progress')
def progress_page():
    return render_template('progress.html')

@app.route('/progress/log')
def progress_log_page():
    return render_template('progress_log.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or request.form.to_dict()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Both fields are required.'}), 400

    if users.get(username) == password:
        return jsonify({'success': True, 'message': 'Login successful'})
    return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

@app.route('/api/signup', methods=['POST'])
def api_signup():
    data = request.get_json(silent=True) or request.form.to_dict()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Both fields are required.'}), 400

    if username in users:
        return jsonify({'success': False, 'message': 'Username already taken.'}), 409

    users[username] = password
    return jsonify({'success': True, 'message': 'Signup successful! Please login.'})

def input_data():
    return request.get_json(silent=True) or request.form.to_dict()

@app.route('/api/notes', methods=['GET'])
def api_get_notes():
    return jsonify({'success': True, 'notes': notes.viewnotes()})

@app.route('/api/notes/add', methods=['POST'])
def api_add_note():
    data = input_data()
    result = notes.addnotes(data.get('note', ''))
    return jsonify(result)

@app.route('/api/notes/search', methods=['POST'])
def api_search_notes():
    data = input_data()
    result = notes.searchnotes(data.get('keyword', ''))
    return jsonify(result)

@app.route('/api/notes/delete', methods=['POST'])
def api_delete_note():
    data = input_data()
    try:
        note_num = int(data.get('note_num', 0))
        result = notes.deletenotes(note_num)
        return jsonify(result)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid note number.'}), 400

@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    return jsonify({'success': True, 'tasks': task_module.load_tasks()})

@app.route('/api/tasks/add', methods=['POST'])
def api_add_task():
    data = input_data()
    result = task_module.add_task(data.get('task', ''))
    return jsonify(result)

@app.route('/api/tasks/toggle', methods=['POST'])
def api_toggle_task():
    data = input_data()
    result = task_module.toggle_task(data.get('task_index', 0))
    return jsonify(result)

@app.route('/api/tasks/delete', methods=['POST'])
def api_delete_task():
    data = input_data()
    result = task_module.delete_task(data.get('task_index', 0))
    return jsonify(result)

@app.route('/api/progress', methods=['GET'])
def api_get_progress():

    data = progress.load_logged_data()

    plot_url = progress.plot_average_study_time(data)

    sessions = []

    for date in sorted(data.keys(), reverse=True):

        for hours in data[date]:

            sessions.append({
                "date": date,
                "hours": hours
            })

    return jsonify({
        'success': True,
        'sessions': sessions,
        'plot_url': plot_url
    })

@app.route('/api/progress/log', methods=['POST'])
def api_log_progress():
    data = input_data()
    result = progress.log_study_session(data.get('date', ''), data.get('hours', ''))
    return jsonify(result)

@app.route('/pomodoro/start', methods=['POST'])
def start_pomodoro_timer():
    data = input_data()
    result = pomodoro.start_pomodoro(data.get('minutes', 0))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
