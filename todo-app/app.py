# app.py is the main Python file and runs Flask
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

from database import (
    get_db_connection,
    add_task,
    get_task,
    update_task,
    delete_task,
    restore_task,
    toggle_task
)

app = Flask(__name__)

# Date formatter
@app.template_filter('format_date')
def format_date(date_str):
    if not date_str:
        return None
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return d.strftime("%A, %b %d")

# Time formatter
@app.template_filter('format_time')
def format_time(time_str):
    if not time_str:
        return None
    
    time_obj = datetime.strptime(time_str, "%H:%M")
    return time_obj.strftime("%I:%M %p")

# For the home interface
@app.route('/')
def index():
    tab = request.args.get('tab', 'all')
    view_mode = request.args.get('view', 'list')

    conn = get_db_connection()

    all_tasks = conn.execute('SELECT * FROM tasks').fetchall()
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
    tasks = conn.execute(query).fetchall()
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

        due = datetime.strptime(t['due_date'], "%Y-%m-%d").date()
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
def add():
    
    title = request.form['title']
    due_date = request.form['due_date']
    due_time = request.form['due_time']
    priority = request.form['priority']
    tag = request.form['tag']

    
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
def toggle(task_id):
    toggle_task(task_id) 
    
    return redirect(url_for('index'))

# For deleting tasks
@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete(task_id):
    delete_task(task_id)
    return '', 204

# For deleting tasks
@app.route('/restore/<int:task_id>', methods=['POST'])
def restore(task_id):
    restore_task(task_id)
    return '', 204

# For editing task and updating values of edited tasks
@app.route('/edit/<int:task_id>', methods=['POST'])
def update(task_id):
    title = request.form['title']
    due_date = request.form['due_date']
    due_time = request.form['due_time']
    priority = request.form['priority']
    tag = request.form['tag']
    
    update_task(
        task_id,
        title,
        due_date,
        due_time,
        priority,
        tag
    )
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)   