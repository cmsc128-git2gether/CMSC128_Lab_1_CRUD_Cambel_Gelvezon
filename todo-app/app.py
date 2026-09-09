from asyncio import tasks
from flask import Flask, render_template, request
from database import get_db_connection, init_db
from datetime import datetime, timedelta

app = Flask(__name__)

@app.template_filter('format_date')
def format_date(date_str):
    if not date_str:
        return None
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return d.strftime("%A, %b %d")

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
    query += ' ORDER BY due_date ASC'

    tasks = conn.execute(query).fetchall()
    conn.close()

    today = datetime.now().date()

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

    # only include non-empty groups, keeps template logic simple
    grouped_open = []
    if today_tasks:
        grouped_open.append(("Today", today_tasks))
    if no_due_date_tasks:
        grouped_open.append(("No Due Date", no_due_date_tasks))
    if upcoming_tasks:
        grouped_open.append(("Upcoming", upcoming_tasks))

    def fmt(d):
        return d.strftime("%b %d").replace(" 0", " ")

    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    date_range = f"{fmt(start_of_week)} - {end_of_week.day}, {end_of_week.year}"

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

if __name__ == '__main__':
    app.run(debug=True)