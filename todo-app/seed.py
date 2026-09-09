"""
Seeder script for the todo-app tasks table.

Usage:
    python seed.py

Requires database.py (get_db_connection, init_db) to be importable
from the same directory as this script — matches your app.py setup.
"""

from database import get_db_connection, init_db

# (title, due_date, priority, tag, completed)
TASKS = [
    ("Request booking CMSC124", "2026-09-12", "Med", "Others", 0),
    ("Finish wireframe and schema design", "2026-09-13", "High", "School", 0),
    ("Pick up dry cleaning", "2026-09-10", "Low", "Personal", 0),
    ("Prepare sprint planning slides", "2026-09-09", "High", "Others", 0),
    ("Call internet provider", "2026-09-11", "Med", "Personal", 0),
    ("Backup hard drive", "2026-09-14", "Low", "Others", 0),
    ("Finish algorithms homework", "2026-09-10", "High", "School", 0),
    ("Group project check-in", "2026-09-12", "Med", "School", 0),
    ("Buy groceries", "2026-09-09", "Low", "Personal", 0),
    ("Renew library card", "2026-09-15", "Low", "Others", 0),
    ("Review design system docs", "2026-09-08", "Med", "Others", 1),
    ("Schedule quarterly review", "2026-09-09", "Med", "Others", 1),
    ("Renew gym membership", "2026-09-11", "Low", "Personal", 1),
    ("kms", "", "High", "Personal", 0),
]


def seed():
    init_db()  # ensures the table exists / is reset, per your database.py setup
    conn = get_db_connection()

    conn.executemany(
        """
        INSERT INTO tasks (title, due_date, priority, tag, completed)
        VALUES (?, ?, ?, ?, ?)
        """,
        TASKS,
    )

    conn.commit()
    conn.close()
    print(f"Seeded {len(TASKS)} tasks.")


if __name__ == "__main__":
    seed()