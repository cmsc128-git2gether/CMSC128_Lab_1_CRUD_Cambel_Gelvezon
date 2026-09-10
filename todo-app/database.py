# database.py communicates with SQLite
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'todo.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    schema_path = os.path.join(
        os.path.dirname(__file__),
        'schema.sql'
    )

    with open(schema_path) as f:
        schema = f.read()
        
    conn = get_db_connection()
    conn.executescript(schema)
    conn.close()

# Adding a task
def add_task(title, due_date, due_time, priority, tag):
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title, due_date, due_time, priority, tag) VALUES (?, ?, ?, ?, ?)',
                 (title, due_date, due_time, priority, tag))
    conn.commit()
    conn.close()

# Returns one single task based on the task_id
# If task_id does not exist, fetchone() will return None
def get_task(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    return task

# Returns all tasks in the database
def get_all_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks ORDER BY completed ASC, due_date ASC, due_time ASC, created_at DESC').fetchall()
    conn.close()
    return tasks    

# Update edited tasks
def update_task(task_id, title, due_date, due_time, priority, tag):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET title = ?, due_date = ?, due_time = ?, priority = ?, tag = ? WHERE id = ?',
                 (title, due_date, due_time, priority, tag, task_id))
    conn.commit()
    conn.close()

# Delete data using id
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# Mark data as complete 
def toggle_task(task_id):
    conn = get_db_connection()
    conn.execute('''
                UPDATE tasks 
                SET completed = CASE
                    WHEN completed = 0 THEN 1 
                    ELSE 0
                END
                WHERE id = ?''',
                (task_id,))
    conn.commit()
    conn.close()
