# database.py communicates with MySQL
import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv(
    os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        ".env"
    )
)

# MySQL configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": "todo_app"
}


def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)

        if conn.is_connected():
            return conn

    except Error as e:
        print(f"Database connection error: {e}")

    return None


# Initialize database
def init_db():
    with open("schema.sql", "r") as f:
        schema = f.read()

    conn = get_db_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    # schema.sql contains multiple statements
    for statement in schema.split(";"):
        statement = statement.strip()

        if statement:
            cursor.execute(statement)

    conn.commit()

    cursor.close()
    conn.close()


# Adding a task
def add_task(title, due_date, due_time, priority, tag):
    conn = get_db_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks
        (title, due_date, due_time, priority, tag)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (title, due_date, due_time, priority, tag)
    )

    conn.commit()

    cursor.close()
    conn.close()


# Returns one single task based on task_id
def get_task(task_id):
    conn = get_db_connection()

    if conn is None:
        return None

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    cursor.close()
    conn.close()

    return task


# Returns all tasks
def get_all_tasks():
    conn = get_db_connection()

    if conn is None:
        return []

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM tasks
        ORDER BY completed ASC, due_date ASC, due_time ASC, created_at DESC
        """
    )

    tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return tasks


# Update edited tasks
def update_task(task_id, title, due_date, due_time, priority, tag):
    conn = get_db_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = %s,
            due_date = %s,
            due_time = %s,
            priority = %s,
            tag = %s
        WHERE id = %s
        """,
        (title, due_date, due_time, priority, tag, task_id)
    )

    conn.commit()

    cursor.close()
    conn.close()


# Delete task
def delete_task(task_id):
    conn = get_db_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()


# Mark task as complete / incomplete
def toggle_task(task_id):
    conn = get_db_connection()

    if conn is None:
        return

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = CASE
            WHEN completed = 0 THEN 1
            ELSE 0
        END
        WHERE id = %s
        """,
        (task_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()