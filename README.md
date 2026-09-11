# Tutuman — Todo App

A lightweight, task-management web app built with vanilla HTML/CSS/JS on the frontend and Flask + SQLite on the backend.

## Tech Stack

| Layer      | Choice                  | Why                                                                                                                                                                                |
| ---------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Backend    | **Flask** (Python)      | Lightweight, minimal boilerplate for a small CRUD app; Jinja templating built in, so no separate frontend framework/build step needed.                                             |
| Database   | **SQLite**              | File-based, zero-config — no separate DB server to install or run. Well suited to a single-user local app and to `sqlite3`'s built-in Python support (no extra driver dependency). |
| Frontend   | **Vanilla HTML/CSS/JS** | No framework overhead for a project this size; direct DOM manipulation and `fetch()` calls are enough to cover modals, filtering, and delete/undo without adding a build pipeline. |
| Templating | **Jinja2** (via Flask)  | Server-rendered HTML keeps state (tasks, filters, active tab) driven by the URL/query params, avoiding client-side state duplication.                                              |

**Data model** (`schema.sql`):

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    due_date TEXT,
    due_time TEXT,
    priority TEXT NOT NULL DEFAULT 'Low' CHECK (priority IN ('Low', 'Med', 'High')),
    tag TEXT NOT NULL DEFAULT 'Others' CHECK (tag IN ('School', 'Personal', 'Others')),
    completed INTEGER NOT NULL DEFAULT 0,
    deleted INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

Deletes are **soft deletes** (`deleted` flag) rather than hard `DELETE` statements, so a task can be restored via the undo toast for a short window after deletion instead of being immediately unrecoverable.

## Running Locally

**Requirements:** Python 3.9+

1. **Clone/download the project**, then open a terminal in the project root (the folder containing `app.py`).

2. **Create and activate a virtual environment** (recommended, not required):

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install flask
   ```

   _(If a `requirements.txt` exists in the project, use `pip install -r requirements.txt` instead.)_

4. **Initialize the database:**

   ```bash
   python -c "from database import init_db; init_db()"
   ```

   This creates `todo.db` using `schema.sql`. **Warning:** re-running this drops and recreates the `tasks` table, wiping existing data — only do this on first setup or when you intend to reset.

5. **(Optional) Seed sample data:**

   ```bash
   python seed.py
   ```

6. **Run the app:**

   ```bash
   python app.py
   ```

7. Open **http://127.0.0.1:5000** in your browser.

## Data Operations (Flask Routes)

All routes are defined in `app.py` and talk to SQLite through helper functions in `database.py`.

| Method   | Route                     | Purpose                                                                                                                                                                |
| -------- | ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `GET`    | `/`                       | Renders the task list. Supports query params: `tab` (`all` / `ongoing` / `completed`), `view` (`list` / `calendar`), `priority`, `tag` — all combinable for filtering. |
| `POST`   | `/add`                    | Creates a new task from form fields: `title`, `due_date`, `due_time`, `priority`, `tag`.                                                                               |
| `POST`   | `/complete/<int:task_id>` | Toggles a task's `completed` status (used for both marking done and marking ongoing again).                                                                            |
| `POST`   | `/edit/<int:task_id>`     | Updates an existing task's fields.                                                                                                                                     |
| `DELETE` | `/delete/<int:task_id>`   | Soft-deletes a task (`deleted = 1`). Called via `fetch()` from the frontend, not a form, so it returns `204 No Content` rather than redirecting.                       |
| `POST`   | `/restore/<int:task_id>`  | Reverses a soft delete (`deleted = 0`) — powers the "Undo" button on the delete toast.                                                                                 |

## Screenshots
<img width="1917" height="927" alt="task-list" src="https://github.com/user-attachments/assets/73646e9d-b627-434b-86ba-63bc7ca988f1" />
<img width="1917" height="926" alt="undo-toast" src="https://github.com/user-attachments/assets/066239e3-2e13-47f3-a506-2d05ee686e7e" />
<img width="1917" height="927" alt="Screenshot 2026-09-11 234521" src="https://github.com/user-attachments/assets/f75d4cf0-8e37-4a44-8cf0-9739c9f016c2" />
<img width="1917" height="930" alt="new-task-modal" src="https://github.com/user-attachments/assets/19007602-424b-4e4a-9618-8fdb7b240421" />
<img width="1917" height="923" alt="delete-confirm" src="https://github.com/user-attachments/assets/03eb2f5e-b4a2-4bff-b981-d9d9dfd59197" />
