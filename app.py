from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
import uuid
import hashlib
import secrets

app = Flask(__name__)
CORS(app)

# Configure session
app.config['SECRET_KEY'] = secrets.token_hex(32)

# In-memory storage (in production, use a proper database)
tasks = []
todos = []
timer_sessions = []
users = []

# Load data from JSON files if they exist
TASKS_FILE = 'data/tasks.json'
TODOS_FILE = 'data/todos.json'
SESSIONS_FILE = 'data/sessions.json'
USERS_FILE = 'data/users.json'

def ensure_data_directory():
    """Ensure data directory exists"""
    os.makedirs('data', exist_ok=True)

def load_data():
    """Load tasks, todos, sessions, and users from files"""
    global tasks, todos, timer_sessions, users
    ensure_data_directory()
    
    try:
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as f:
                tasks = json.load(f)
    except Exception as e:
        print(f"Error loading tasks: {e}")
        tasks = []
    
    try:
        if os.path.exists(TODOS_FILE):
            with open(TODOS_FILE, 'r') as f:
                todos = json.load(f)
    except Exception as e:
        print(f"Error loading todos: {e}")
        todos = []
    
    try:
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, 'r') as f:
                timer_sessions = json.load(f)
    except Exception as e:
        print(f"Error loading sessions: {e}")
        timer_sessions = []
    
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                users = json.load(f)
    except Exception as e:
        print(f"Error loading users: {e}")
        users = []

def save_data():
    """Save tasks, todos, sessions, and users to files"""
    ensure_data_directory()
    
    try:
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)
    except Exception as e:
        print(f"Error saving tasks: {e}")
    
    try:
        with open(TODOS_FILE, 'w') as f:
            json.dump(todos, f, indent=2)
    except Exception as e:
        print(f"Error saving todos: {e}")
    
    try:
        with open(SESSIONS_FILE, 'w') as f:
            json.dump(timer_sessions, f, indent=2)
    except Exception as e:
        print(f"Error saving sessions: {e}")
    
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        print(f"Error saving users: {e}")

# Authentication helper functions
def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return hash_password(password) == hashed

def is_authenticated():
    """Check if user is authenticated"""
    return 'user_id' in session

def get_current_user():
    """Get current user from session"""
    if not is_authenticated():
        return None
    user_id = session['user_id']
    return next((u for u in users if u['id'] == user_id), None)

def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    """Serve the main application or redirect to login"""
    if not is_authenticated():
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

# Authentication Routes

@app.route('/login')
def login():
    """Serve login page"""
    if is_authenticated():
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/signup')
def signup():
    """Serve signup page"""
    if is_authenticated():
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Handle user login"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'error': 'Email and password are required'}), 400
    
    email = data['email'].lower().strip()
    password = data['password']
    
    # Find user by email
    user = next((u for u in users if u['email'].lower() == email), None)
    
    if not user or not verify_password(password, user['password_hash']):
        return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
    
    # Set session
    session['user_id'] = user['id']
    session['user_email'] = user['email']
    session['user_name'] = user['name']
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email']
        }
    })

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    """Handle user registration"""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'error': 'Name, email, and password are required'}), 400
    
    name = data['name'].strip()
    email = data['email'].lower().strip()
    password = data['password']
    
    # Validate input
    if len(name) < 2:
        return jsonify({'success': False, 'error': 'Name must be at least 2 characters'}), 400
    
    if len(password) < 6:
        return jsonify({'success': False, 'error': 'Password must be at least 6 characters'}), 400
    
    if '@' not in email:
        return jsonify({'success': False, 'error': 'Invalid email format'}), 400
    
    # Check if user already exists
    if any(u['email'].lower() == email for u in users):
        return jsonify({'success': False, 'error': 'Email already registered'}), 409
    
    # Create new user
    user = {
        'id': str(uuid.uuid4()),
        'name': name,
        'email': email,
        'password_hash': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    users.append(user)
    save_data()
    
    # Set session
    session['user_id'] = user['id']
    session['user_email'] = user['email']
    session['user_name'] = user['name']
    
    return jsonify({
        'success': True,
        'message': 'Account created successfully',
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email']
        }
    })

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """Handle user logout"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

@app.route('/api/auth/me')
def api_get_current_user():
    """Get current user info"""
    if not is_authenticated():
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'created_at': user['created_at']
        }
    })

# Task Management API Endpoints

@app.route('/api/tasks', methods=['GET'])
@require_auth
def get_tasks():
    """Get all tasks or filter by date"""
    current_user = get_current_user()
    date_filter = request.args.get('date')
    project_filter = request.args.get('project')
    status_filter = request.args.get('status')
    
    # Filter tasks by current user
    user_tasks = [t for t in tasks if t.get('user_id') == current_user['id']]
    filtered_tasks = user_tasks.copy()
    
    if date_filter:
        filtered_tasks = [t for t in filtered_tasks if t.get('due_date', '').startswith(date_filter)]
    
    if project_filter:
        filtered_tasks = [t for t in filtered_tasks if t.get('project') == project_filter]
    
    if status_filter:
        filtered_tasks = [t for t in filtered_tasks if t.get('status') == status_filter]
    
    return jsonify({
        'success': True,
        'tasks': filtered_tasks,
        'total': len(user_tasks),
        'filtered': len(filtered_tasks)
    })

@app.route('/api/tasks', methods=['POST'])
@require_auth
def create_task():
    """Create a new task"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'success': False, 'error': 'Task title is required'}), 400
    
    current_user = get_current_user()
    task = {
        'id': str(uuid.uuid4()),
        'user_id': current_user['id'],
        'title': data.get('title'),
        'description': data.get('description', ''),
        'project': data.get('project', 'personal'),
        'priority': data.get('priority', 'medium'),
        'status': data.get('status', 'todo'),
        'due_date': data.get('due_date'),
        'start_time': data.get('start_time'),
        'end_time': data.get('end_time'),
        'location': data.get('location', ''),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'completed': False,
        'completed_at': None
    }
    
    tasks.append(task)
    save_data()
    
    return jsonify({
        'success': True,
        'task': task,
        'message': 'Task created successfully'
    })

@app.route('/api/tasks/<task_id>', methods=['PUT'])
@require_auth
def update_task(task_id):
    """Update an existing task"""
    data = request.get_json()
    current_user = get_current_user()
    
    task_index = next((i for i, t in enumerate(tasks) if t['id'] == task_id), None)
    if task_index is None:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    
    # Check if user owns this task
    if tasks[task_index].get('user_id') != current_user['id']:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    task = tasks[task_index]
    
    # Update fields
    updatable_fields = ['title', 'description', 'project', 'priority', 'status', 
                       'due_date', 'start_time', 'end_time', 'location', 'completed']
    
    for field in updatable_fields:
        if field in data:
            task[field] = data[field]
    
    # Handle completion
    if data.get('completed') and not task.get('completed_at'):
        task['completed_at'] = datetime.now().isoformat()
    elif not data.get('completed'):
        task['completed_at'] = None
    
    task['updated_at'] = datetime.now().isoformat()
    save_data()
    
    return jsonify({
        'success': True,
        'task': task,
        'message': 'Task updated successfully'
    })

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
@require_auth
def delete_task(task_id):
    """Delete a task"""
    global tasks
    current_user = get_current_user()
    
    task_index = next((i for i, t in enumerate(tasks) if t['id'] == task_id), None)
    if task_index is None:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    
    # Check if user owns this task
    if tasks[task_index].get('user_id') != current_user['id']:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    deleted_task = tasks.pop(task_index)
    save_data()
    
    return jsonify({
        'success': True,
        'message': 'Task deleted successfully',
        'deleted_task': deleted_task
    })

# Todo Management API Endpoints

@app.route('/api/todos', methods=['GET'])
@require_auth
def get_todos():
    """Get all todos or filter by date"""
    current_user = get_current_user()
    date_filter = request.args.get('date')
    
    # Filter todos by current user
    user_todos = [t for t in todos if t.get('user_id') == current_user['id']]
    filtered_todos = user_todos.copy()
    
    if date_filter:
        filtered_todos = [t for t in filtered_todos if t.get('date') == date_filter]
    
    return jsonify({
        'success': True,
        'todos': filtered_todos,
        'total': len(user_todos),
        'filtered': len(filtered_todos)
    })

@app.route('/api/todos', methods=['POST'])
@require_auth
def create_todo():
    """Create a new todo"""
    data = request.get_json()
    
    if not data or not data.get('text'):
        return jsonify({'success': False, 'error': 'Todo text is required'}), 400
    
    current_user = get_current_user()
    todo = {
        'id': str(uuid.uuid4()),
        'user_id': current_user['id'],
        'text': data.get('text'),
        'date': data.get('date', datetime.now().date().isoformat()),
        'completed': False,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'completed_at': None
    }
    
    todos.append(todo)
    save_data()
    
    return jsonify({
        'success': True,
        'todo': todo,
        'message': 'Todo created successfully'
    })

@app.route('/api/todos/<todo_id>', methods=['PUT'])
@require_auth
def update_todo(todo_id):
    """Update an existing todo"""
    data = request.get_json()
    current_user = get_current_user()
    
    todo_index = next((i for i, t in enumerate(todos) if t['id'] == todo_id), None)
    if todo_index is None:
        return jsonify({'success': False, 'error': 'Todo not found'}), 404
    
    # Check if user owns this todo
    if todos[todo_index].get('user_id') != current_user['id']:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    todo = todos[todo_index]
    
    # Update fields
    if 'text' in data:
        todo['text'] = data['text']
    if 'completed' in data:
        todo['completed'] = data['completed']
        if data['completed'] and not todo.get('completed_at'):
            todo['completed_at'] = datetime.now().isoformat()
        elif not data['completed']:
            todo['completed_at'] = None
    if 'date' in data:
        todo['date'] = data['date']
    
    todo['updated_at'] = datetime.now().isoformat()
    save_data()
    
    return jsonify({
        'success': True,
        'todo': todo,
        'message': 'Todo updated successfully'
    })

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
@require_auth
def delete_todo(todo_id):
    """Delete a todo"""
    global todos
    current_user = get_current_user()
    
    todo_index = next((i for i, t in enumerate(todos) if t['id'] == todo_id), None)
    if todo_index is None:
        return jsonify({'success': False, 'error': 'Todo not found'}), 404
    
    # Check if user owns this todo
    if todos[todo_index].get('user_id') != current_user['id']:
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    deleted_todo = todos.pop(todo_index)
    save_data()
    
    return jsonify({
        'success': True,
        'message': 'Todo deleted successfully',
        'deleted_todo': deleted_todo
    })

# Calendar API Endpoints

@app.route('/api/calendar/<int:year>/<int:month>')
@require_auth
def get_calendar_data(year, month):
    """Get calendar data for a specific month"""
    from calendar import monthrange
    
    # Get first and last day of the month
    first_day = datetime(year, month, 1)
    last_day_num = monthrange(year, month)[1]
    last_day = datetime(year, month, last_day_num)
    
    # Get tasks for this month (filtered by current user)
    current_user = get_current_user()
    month_tasks = []
    for task in tasks:
        if task.get('user_id') == current_user['id'] and task.get('due_date'):
            try:
                task_date = datetime.fromisoformat(task['due_date'].replace('Z', '+00:00'))
                if first_day <= task_date <= last_day:
                    month_tasks.append(task)
            except:
                continue
    
    return jsonify({
        'success': True,
        'year': year,
        'month': month,
        'tasks': month_tasks,
        'month_name': first_day.strftime('%B'),
        'days_in_month': last_day_num,
        'first_day_weekday': first_day.weekday()
    })

# Timer API Endpoints

@app.route('/api/timer/start', methods=['POST'])
@require_auth
def start_timer():
    """Start a timer session"""
    data = request.get_json()
    
    current_user = get_current_user()
    session = {
        'id': str(uuid.uuid4()),
        'user_id': current_user['id'],
        'type': data.get('type', 'focus'),  # focus, break
        'duration_minutes': data.get('duration_minutes', 25),
        'task_id': data.get('task_id'),
        'started_at': datetime.now().isoformat(),
        'completed': False
    }
    
    timer_sessions.append(session)
    save_data()
    
    return jsonify({
        'success': True,
        'session': session,
        'message': 'Timer started successfully'
    })

@app.route('/api/timer/complete/<session_id>', methods=['POST'])
@require_auth
def complete_timer_session(session_id):
    """Complete a timer session"""
    session_index = next((i for i, s in enumerate(timer_sessions) if s['id'] == session_id), None)
    if session_index is None:
        return jsonify({'success': False, 'error': 'Session not found'}), 404
    
    session = timer_sessions[session_index]
    session['completed'] = True
    session['completed_at'] = datetime.now().isoformat()
    
    # Calculate actual duration
    started_at = datetime.fromisoformat(session['started_at'])
    completed_at = datetime.fromisoformat(session['completed_at'])
    actual_duration = (completed_at - started_at).total_seconds() / 60
    session['actual_duration_minutes'] = round(actual_duration, 2)
    
    save_data()
    
    return jsonify({
        'success': True,
        'session': session,
        'message': 'Timer session completed'
    })

@app.route('/api/timer/sessions')
@require_auth
def get_timer_sessions():
    """Get timer sessions"""
    current_user = get_current_user()
    date_filter = request.args.get('date')
    
    # Filter sessions by current user
    user_sessions = [s for s in timer_sessions if s.get('user_id') == current_user['id']]
    filtered_sessions = user_sessions.copy()
    
    if date_filter:
        filtered_sessions = [s for s in filtered_sessions 
                           if s.get('started_at', '').startswith(date_filter)]
    
    return jsonify({
        'success': True,
        'sessions': filtered_sessions,
        'total': len(user_sessions)
    })

# Analytics API Endpoints

@app.route('/api/analytics/productivity')
@require_auth
def get_productivity_analytics():
    """Get productivity analytics"""
    current_user = get_current_user()
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Filter data by current user
    user_tasks = [t for t in tasks if t.get('user_id') == current_user['id']]
    user_sessions = [s for s in timer_sessions if s.get('user_id') == current_user['id']]
    
    # Calculate task completion rates
    total_tasks = len(user_tasks)
    completed_tasks = len([t for t in user_tasks if t.get('completed')])
    
    # Tasks created this week
    week_tasks = []
    for task in user_tasks:
        try:
            created_at = datetime.fromisoformat(task['created_at']).date()
            if created_at >= week_ago:
                week_tasks.append(task)
        except:
            continue
    
    # Timer sessions this week
    week_sessions = []
    for session in user_sessions:
        try:
            started_at = datetime.fromisoformat(session['started_at']).date()
            if started_at >= week_ago:
                week_sessions.append(session)
        except:
            continue
    
    # Calculate focus time this week
    total_focus_time = sum(
        s.get('actual_duration_minutes', s.get('duration_minutes', 0))
        for s in week_sessions if s.get('type') == 'focus' and s.get('completed')
    )
    
    return jsonify({
        'success': True,
        'analytics': {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1),
            'tasks_this_week': len(week_tasks),
            'focus_sessions_this_week': len([s for s in week_sessions if s.get('type') == 'focus']),
            'total_focus_time_minutes': round(total_focus_time, 1),
            'average_session_length': round(
                sum(s.get('actual_duration_minutes', 0) for s in week_sessions if s.get('completed')) / 
                len([s for s in week_sessions if s.get('completed')]) if week_sessions else 0, 1
            )
        }
    })

# Search API

@app.route('/api/search')
@require_auth
def search_tasks():
    """Search tasks"""
    current_user = get_current_user()
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'success': True, 'results': []})
    
    # Filter tasks by current user
    user_tasks = [t for t in tasks if t.get('user_id') == current_user['id']]
    
    results = []
    for task in user_tasks:
        if (query in task.get('title', '').lower() or 
            query in task.get('description', '').lower() or
            query in task.get('project', '').lower()):
            results.append(task)
    
    return jsonify({
        'success': True,
        'query': query,
        'results': results,
        'count': len(results)
    })

# Health check endpoint

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    load_data()
    print("🎉 Toodless Python Backend Starting...")
    print("📊 Features:")
    print("  ✅ Task Management API")
    print("  📅 Calendar Integration")
    print("  ⏱️  Focus Timer")
    print("  📈 Productivity Analytics")
    print("  🔍 Search Functionality")
    print("")
    print("🌐 Access your app at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
