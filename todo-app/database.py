import sqlite3

DATABASE = 'todo.db' #final database w/ logic

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_db_connection()
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
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

# epdate edited tasks
def update_task(task_id, title, due_date, due_time, priority, tag):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET title = ?, due_date = ?, due_time = ?, priority = ?, tag = ? WHERE id = ?',
                 (title, due_date, due_time, priority, tag, task_id))
    conn.commit()
    conn.close()

# delete data using id
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

# mark data as complete 
def complete_task(task_id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
