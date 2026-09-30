# app.py is the main Python file and runs Flask
import os
import re
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from mysql.connector import IntegrityError

from database import (
    get_db_connection,
    add_task,
    get_task,
    update_task,
    delete_task,
    toggle_task,
    get_user_by_email,
    get_user_by_id,
    create_user
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(days=7)

# checks if user is logged in 
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

# format dates
@app.template_filter('format_date')
def format_date(date_value):
    if not date_value:
        return None

    if isinstance(date_value, str):
        date_value = datetime.strptime(date_value, "%Y-%m-%d").date()

    return date_value.strftime("%A, %b %d")

# Time formatter
@app.template_filter('format_time')
def format_time(time_value):
    if not time_value:
        return None

    if isinstance(time_value, str):
        time_obj = datetime.strptime(time_value, "%H:%M").time()
    elif isinstance(time_value, timedelta):
        # MySQL TIME values are returned as timedelta
        total_seconds = int(time_value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        time_obj = datetime.strptime(
            f"{hours:02d}:{minutes:02d}",
            "%H:%M"
        ).time()
    else:
        time_obj = time_value

    return time_obj.strftime("%I:%M %p")

# For the home interface
@app.route('/tasks')
@login_required
def index():
    tab = request.args.get('tab', 'all')
    view_mode = request.args.get('view', 'list')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks")
    all_tasks = cursor.fetchall()
    total_count = len(all_tasks)
    open_count = sum(1 for t in all_tasks if t['completed'] == 0)
    done_count = sum(1 for t in all_tasks if t['completed'] == 1)

    query = 'SELECT * FROM tasks WHERE 1=1'
    if tab == 'ongoing':
        query += ' AND completed = 0'
    elif tab == 'completed':
        query += ' AND completed = 1'
        
    # Displays tasks in a specific order
    query += ''' 
        ORDER BY
            due_date ASC,
            CASE priority
                WHEN 'High' THEN 1
                WHEN 'Med' THEN 2
                WHEN 'Low' THEN 3
            END ASC,
            due_date ASC,
            due_time ASC
    '''
    cursor.execute(query)
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    today = datetime.now().date()
    
    # For pedning and completed tasks
    open_tasks = [t for t in tasks if t['completed'] == 0]
    done_tasks = [t for t in tasks if t['completed'] == 1]

    today_tasks = []
    upcoming_tasks = []
    no_due_date_tasks = []

    for t in open_tasks:
        if not t['due_date']:
            no_due_date_tasks.append(t)
            continue

        due = t['due_date']

        if isinstance(due, str):
            due = datetime.strptime(due, "%Y-%m-%d").date()
            
        if due <= today:
            # overdue tasks are folded into "Today" so nothing open silently disappears
            today_tasks.append(t)
        else:
            upcoming_tasks.append(t)

    # Only include non-empty groups, keeps template logic simple
    grouped_open = []
    if today_tasks:
        grouped_open.append(("Today", today_tasks))
    if no_due_date_tasks:
        grouped_open.append(("No Due Date", no_due_date_tasks))
    if upcoming_tasks:
        grouped_open.append(("Upcoming", upcoming_tasks))

    # Week-Date Range
    def fmt(d):
        return d.strftime("%b %d").replace(" 0", " ")

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    date_range = f"{fmt(start_of_week)} - {end_of_week.day}, {end_of_week.year}"

    # Direct to index.html
    return render_template(
        'index.html',
        grouped_open=grouped_open,
        done_tasks=done_tasks,
        today_tasks=today_tasks,
        tab=tab,
        view_mode=view_mode,
        total_count=total_count,
        open_count=open_count,
        done_count=done_count,
        date_range=date_range
    )

# For adding tasks
@app.route('/add', methods=['POST'])
@login_required
def add():
    
    title = request.form['title']
    due_date = request.form.get('due_date') or None
    due_time = request.form.get('due_time') or None
    priority = request.form.get('priority') or None
    tag = request.form.get('tag') or None

    
    add_task(
        title,
        due_date,
        due_time, 
        priority,
        tag
    )
    
    return redirect(url_for('index'))
   
# For completing tasks
@app.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def toggle(task_id):
    toggle_task(task_id) 
    
    return redirect(url_for('index'))

# For deleting tasks
@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete(task_id):
    delete_task(task_id) 
    
    return redirect(url_for('index'))

# For editing task and updating values of edited tasks
@app.route('/edit/<int:task_id>', methods=['POST'])
@login_required
def update(task_id):
    title = request.form['title']
    due_date = request.form.get('due_date') or None
    due_time = request.form.get('due_time') or None
    priority = request.form.get('priority') or None
    tag = request.form.get('tag') or None
    
    update_task(
        task_id,
        title,
        due_date,
        due_time,
        priority,
        tag
    )
    
    return redirect(url_for('index'))

# --------- LAB 2 FUNCTIONS --------- #

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD_LENGTH = 8

@app.route('/')
def home():
    if "user_id" in session:
        return redirect(url_for("profile"))
    return redirect(url_for("login"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    # show form on GET method
    if request.method == 'GET':
        return render_template('register.html')
    
    # read form on POST method
    # TODO: implement added requirements for password (e.g must include sysmbols, etc)
    email = request.form.get('email', '').strip().lower()
    display_name = request.form.get('display_name', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # form validation
    error = None 
    if not email or not display_name or not password or not confirm_password:
        error = "All fields are required."
    elif not EMAIL_PATTERN.match(email):
        error = "Please enter a valid email address."
    elif len(password) < MIN_PASSWORD_LENGTH:
        error = f"Password must be at least {MIN_PASSWORD_LENGTH} characters."
    elif password != confirm_password:
        error = "Passwords do not match."
    elif get_user_by_email(email):
        error = "An account with that email already exists."
        
    if error:
        flash(error, "error")
        return render_template('register.html', email=email, display_name=display_name)
    
    # hash password and save user
    password_hash = generate_password_hash(password)
    try:
        create_user(email, display_name, password_hash)
    except IntegrityError:
        # registering using same email causes errors
        flash("An account with that email already exists.", "error")
        return render_template('register.html', email=email, display_name=display_name)
    
    # redirect to login on successful register
    flash("Account created. Please log in.", "success")
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('/login.html')

@app.route('/profile')
def profile():
    user = get_user_by_id(session["user_id"])
    if user is None:
        session.clear()
        return redirect(url_for("login"))
    return render_template('profile.html', user=user)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)   