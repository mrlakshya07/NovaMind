import os
import sys
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from dotenv import load_dotenv
from supabase_client import supabase
from auth_service import get_current_user, login_required, signup, login, logout
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import notes
import study_progress_tracker as progress
import pomodoro
import tasks as task_module
import achievements

FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

TEMPLATE_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path='/static'
)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# ============================================================================
# PUBLIC ROUTES (Authentication Pages)
# ============================================================================

@app.route('/login')
def login_page():
    """Render login page"""
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    """Render signup page"""
    return render_template('signup.html')

@app.route('/')
def index():
    """Homepage - redirect to login if not authenticated"""
    if not get_current_user():
        return redirect(url_for('login_page'))
    return render_template('index.html')

# ============================================================================
# AUTHENTICATION API ENDPOINTS
# ============================================================================

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    """User signup endpoint"""
    data = request.get_json(silent=True) or request.form.to_dict()
    
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    username = data.get('username', '').strip()
    
    # Validation
    if not email or not password or not username:
        return jsonify({
            'success': False,
            'message': 'Email, password, and username are required.'
        }), 400
    
    if len(password) < 6:
        return jsonify({
            'success': False,
            'message': 'Password must be at least 6 characters.'
        }), 400
    
    if len(username) < 2:
        return jsonify({
            'success': False,
            'message': 'Username must be at least 2 characters.'
        }), 400
    
    result = signup(email, password, username)
    status_code = 200 if result['success'] else 400
    return jsonify(result), status_code


@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """User login endpoint"""
    data = request.get_json(silent=True) or request.form.to_dict()
    
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return jsonify({
            'success': False,
            'message': 'Email and password are required.'
        }), 400
    
    result = login(email, password)
    status_code = 200 if result['success'] else 401
    return jsonify(result), status_code


@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """User logout endpoint"""
    result = logout()
    return jsonify(result), 200


@app.route('/api/auth/me', methods=['GET'])
@login_required
def api_current_user():
    """Get current authenticated user"""
    user = get_current_user()
    return jsonify({
        'success': True,
        'user': user
    }), 200

# ============================================================================
# PROTECTED ROUTES (Require Authentication)
# ============================================================================

@app.route('/notes')
def notes_page():
    if not get_current_user():
        return redirect(url_for('login_page'))
    return render_template('notes.html')

@app.route('/tasks')
def tasks_page():
    if not get_current_user():
        return redirect(url_for('login_page'))
    return render_template('tasks.html')

@app.route('/pomodoro')
def pomodoro_page():
    if not get_current_user():
        return redirect(url_for('login_page'))
    return render_template('pomodoro.html')

@app.route('/progress')
def progress_page():
    if not get_current_user():
        return redirect(url_for('login_page'))
    return render_template('progress.html')

@app.route('/progress/log')
def progress_log_page():
    if not get_current_user():
        return redirect(url_for('login_page'))
    return render_template('progress_log.html')

@app.route('/achievements')
def achievements_page():
    if not get_current_user():
        return redirect(url_for('login_page'))
    return render_template('achievements.html')

def input_data():
    return request.get_json(silent=True) or request.form.to_dict()

# ============================================================================
# NOTES ENDPOINTS (Protected)
# ============================================================================

@app.route('/api/notes', methods=['GET'])
@login_required
def api_get_notes():
    user = get_current_user()
    return jsonify({'success': True, 'notes': notes.viewnotes(user['user_id'])})

@app.route('/api/notes/add', methods=['POST'])
@login_required
def api_add_note():
    user = get_current_user()
    data = input_data()
    result = notes.addnotes(data.get('note', ''), user['user_id'])
    return jsonify(result)

@app.route('/api/notes/search', methods=['POST'])
@login_required
def api_search_notes():
    user = get_current_user()
    data = input_data()
    result = notes.searchnotes(data.get('keyword', ''), user['user_id'])
    return jsonify(result)

@app.route('/api/notes/delete', methods=['POST'])
@login_required
def api_delete_note():
    user = get_current_user()
    data = input_data()
    try:
        note_num = int(data.get('note_num', 0))
        result = notes.deletenotes(note_num, user['user_id'])
        return jsonify(result)
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Invalid note number.'}), 400

# ============================================================================
# TASKS ENDPOINTS (Protected)
# ============================================================================

@app.route('/api/tasks', methods=['GET'])
@login_required
def api_get_tasks():
    user = get_current_user()
    return jsonify({'success': True, 'tasks': task_module.load_tasks(user['user_id'])})

@app.route('/api/tasks/add', methods=['POST'])
@login_required
def api_add_task():
    user = get_current_user()
    data = input_data()
    result = task_module.add_task(data.get('task', ''), user['user_id'])
    return jsonify(result)

@app.route('/api/tasks/toggle', methods=['POST'])
@login_required
def api_toggle_task():
    user = get_current_user()
    data = input_data()
    # Accept both task_id (new) and task_index (old) for compatibility
    task_id = data.get('task_id') or data.get('task_index')
    result = task_module.toggle_task(task_id, user['user_id'])
    return jsonify(result)

@app.route('/api/tasks/delete', methods=['POST'])
@login_required
def api_delete_task():
    user = get_current_user()
    data = input_data()
    # Accept both task_id (new) and task_index (old) for compatibility
    task_id = data.get('task_id') or data.get('task_index')
    result = task_module.delete_task(task_id, user['user_id'])
    return jsonify(result)

# ============================================================================
# PROGRESS ENDPOINTS (Protected)
# ============================================================================

@app.route('/api/progress', methods=['GET'])
@login_required
def api_get_progress():
    user = get_current_user()
    data = progress.load_logged_data(user['user_id'])

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
@login_required
def api_log_progress():
    user = get_current_user()
    data = input_data()
    result = progress.log_study_session(data.get('date', ''), data.get('hours', ''), user['user_id'])
    if result.get("success"):

        new_achievements = achievements.check_achievements(
            user['user_id']
        )

        result["achievements"] = new_achievements

    return jsonify(result)

# ============================================================================
# POMODORO ENDPOINTS (Protected)
# ============================================================================

@app.route('/api/pomodoro/start', methods=['POST'])
@login_required
def start_pomodoro_timer():
    user = get_current_user()
    data = input_data()
    result = pomodoro.start_pomodoro(data.get('minutes', 0))
    return jsonify(result)

@app.route('/api/pomodoro/complete', methods=['POST'])
@login_required
def complete_pomodoro():
    """Save completed pomodoro session"""
    user = get_current_user()
    data = input_data()
    duration = data.get('duration_minutes', 0)
    focus_score = data.get('focus_score', 100)
    result = pomodoro.save_pomodoro_session(user['user_id'], duration, focus_score)
    return jsonify(result)

@app.route('/api/pomodoro/stats', methods=['GET'])
@login_required
def get_pomodoro_stats():
    """Get pomodoro statistics for user"""
    user = get_current_user()
    stats = pomodoro.get_user_pomodoro_stats(user['user_id'])
    return jsonify({
        'success': True,
        'stats': stats
    })

# ============================================================================
# ACHIEVEMENTS ENDPOINTS (Protected)
# ============================================================================

@app.route('/api/achievements', methods=['GET'])
@login_required
def get_achievements():
    """Get all achievements earned by user"""
    user = get_current_user()
    user_achievements = achievements.get_user_achievements(user['user_id'])
    return jsonify({
        'success': True,
        'achievements': user_achievements
    })

@app.route('/api/achievements/progress', methods=['GET'])
@login_required
def get_achievement_progress():
    """Get progress toward next achievements"""
    user = get_current_user()
    if not user:
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        }), 401
    progress_data = achievements.get_achievement_progress(user['user_id'])
    return jsonify({
        'success': True,
        'progress': progress_data
    })

@app.route('/api/achievements/stats', methods=['GET'])
@login_required
def get_achievement_stats():
    """Get achievement statistics for dashboard"""
    user = get_current_user()
    if not user:
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        }), 401
    stats = achievements.get_achievement_stats(user['user_id'])
    return jsonify({
        'success': True,
        'stats': stats
    })

if __name__ == '__main__':
    app.run(debug=True)