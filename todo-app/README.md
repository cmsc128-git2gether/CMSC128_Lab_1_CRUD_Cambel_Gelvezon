# Tutuman - Todo App

A multi-user todo web app created for organizing,tracking, and categorizing tasks. Each person can register, log in, and manage their own task list.

**Authors:** Cambel, Gelvezon

## Features

- **Account registration and login**: users can sign up by filling in credentials such as email, display name, and passwords.
- **Profile management:** each user has their own profile page with account details and task stats; they can also edit their display name, change their password, or delete their accounts.
- **Secure credentials:** passwords are stored as hash and never as plain text.
- **Task management:** users can create, edit, complete, delete and restore tasks, organized by due date, priority and tag, with views and filters for status.
- **Private task list:** each user has their own task list that others can't see.
- **Persistent sessions:** users stay logged in across refreshes and browser restarts, and pages are protected when signed out.
- **Password recovery**: emails will be sent to users registered emails that allow them to reset their passwords.

## Tech stack

| Layer          | Choice                                                                                                                                                               |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Frontend       | Server-rendered Jinja2 templates, plain HTML, CSS (custom properties and nesting), and vanilla JavaScript. Bootstrap Icons and the DM Sans font are loaded from CDNs |
| Backend        | Python 3 with Flask                                                                                                                                                  |
| Database       | MySQL (XAMPP / MariaDB), accessed with `mysql-connector-python` and parameterized queries                                                                            |
| Authentication | Session-based login. Passwords are hashed with Werkzeug (`generate_password_hash` / `check_password_hash`). Sessions are signed cookies                              |
| Testing        | pytest with Flask's test client                                                                                                                                      |

## Project structure

```
todo-app/
├── app.py            # Flask app and all routes
├── database.py       # MySQL connection and every database operation
├── schema.sql        # Table definitions
├── .env              # Local secrets (not committed)
├── .env.example      # Names of the required variables
├── templates/        # index, login, register, profile
├── static/
│   ├── css/
│   └── js/
└── tests/            # pytest tests
```

## Installation and local run

**Requirements:** Python 3.10+, XAMPP (for MySQL), and a browser.

1. **Clone the repository** and open the project folder.
2. **Install the dependencies:**

```bash
   python -m pip install flask mysql-connector-python python-dotenv
```

For the tests, also run `python -m pip install pytest`.

3. **Create a `.env` file** next to `app.py`:

```
   MYSQL_PASSWORD=
   SECRET_KEY=your-long-random-string
```

- Leave `MYSQL_PASSWORD` empty if your XAMPP MySQL has no password (the default).
- Generate a secret key with:

```bash
     python -c "import secrets; print(secrets.token_hex(32))"
```

- `.env` is listed in `.gitignore`. Never commit it.

4. **Set up the database** (see the next section).
5. **Start MySQL** in the XAMPP Control Panel.
6. **Run the app:**

```bash
   python app.py
```

Open **http://127.0.0.1:5000**. You'll be sent to the login page.

To run the tests (MySQL must be running):

```bash
python -m pytest -v
```

The tests create accounts with the email domain `@test.invalid` and delete them before and after each test.

## Database setup
 
1. Start **MySQL** (and Apache, if you want phpMyAdmin) in XAMPP.
2. Open `http://localhost/phpmyadmin` and create a database named **`todo_app`**.
3. Select `todo_app`, open the **Import** tab (or the **SQL** tab), and run `schema.sql`.
> `schema.sql` starts with `DROP TABLE IF EXISTS`, so running it again deletes all existing accounts and tasks.
 
The database connection settings (host `localhost`, user `root`, database `todo_app`) are in `DB_CONFIG` in `database.py`. The password comes from `.env`.
 
**Tables**
 
| Table | Columns |
|---|---|
| `users` | `id` (PK), `email` (unique), `display_name`, `password_hash`, `created_at` |
| `tasks` | `id` (PK), `user_id` (FK to `users.id`, `ON DELETE CASCADE`), `title`, `due_date`, `due_time`, `priority`, `tag`, `completed`, `deleted`, `created_at` |

## Routes and database operations
 
**Authentication and account**
 
| Method | Route | Description | Auth |
|---|---|---|---|
| GET | `/` | Redirects to `/profile` if logged in, otherwise `/login` | No |
| GET, POST | `/register` | Show the form; validate, hash the password, and create the user | No |
| GET, POST | `/login` | Show the form; verify the password hash and start a session | No |
| POST | `/logout` | Clear the session | Yes |
| GET | `/profile` | Greeting, account details, and activity counts | Yes |
| POST | `/profile/edit` | Update the display name | Yes |
| POST | `/profile/password` | Change the password (needs the current password) | Yes |
| POST | `/profile/delete` | Delete the account and its tasks | Yes |
 
**Tasks** (all require login and only touch the current user's tasks)
 
| Method | Route | Description |
|---|---|---|
| GET | `/tasks` | List tasks. Query parameters: `tab`, `view`, `priority`, `tag` |
| POST | `/add` | Create a task |
| POST | `/edit/<id>` | Update a task |
| POST | `/complete/<id>` | Toggle completed |
| POST | `/delete/<id>` | Soft delete a task |
| POST | `/restore/<id>` | Restore a soft-deleted task |
 
**Database operations** (`database.py`)
 
- Users: `create_user`, `get_user_by_email`, `get_user_by_id`, `update_display_name`, `update_password_hash`, `delete_user`
- Tasks: `add_task`, `get_task`, `get_all_tasks`, `update_task`, `delete_task`, `restore_task`, `toggle_task`, `get_task_stats`
Every task function takes a `user_id` and includes it in its `WHERE` clause, so changing an ID in a URL can't read or modify another user's task. All queries use `%s` placeholders to prevent SQL injection.
 
## Session mechanism
 
- **Storage:** Flask's `session` is a cookie in the browser holding the user's ID. The cookie is signed with `SECRET_KEY`, so it can't be changed without the key. The server stores no session data, which is why restarting the server doesn't log anyone out.
- **Login:** after the password hash is verified, the session is cleared (to discard any older session), the user's ID is stored, and `session.permanent = True` is set.
- **Persistence:** permanent sessions get an expiry date of **7 days** (`app.permanent_session_lifetime`), so the login survives page refreshes and browser restarts. The 7 days count from the user's last request.
- **Route protection:** a `login_required` decorator redirects to `/login` when there is no user ID in the session. It's applied to the profile and all task routes, and `/login` and `/register` redirect logged-in users to the profile.
- **Logout:** a POST request clears the session and returns to `/login`.
- **Expiry:** the session also ends if the user clears their cookies, if `SECRET_KEY` changes, or after 7 days without a visit.

## Password hashing
 
Passwords are hashed with Werkzeug's `generate_password_hash`, which adds a random salt (the algorithm is scrypt or pbkdf2, depending on the installed version). The plain password is never stored or logged. Login compares the entered password against the stored hash with `check_password_hash`. The failure message is the same for an unknown email and a wrong password.
 
## Password recovery

Password reset tokens are generated and stored in the database as SHA-256 hashes, rather than the original tokens. The reset link containing the original token is sent to the user's registered email through SMTP, and it expires after 30 minutes. Once verified, user can set a new password, which is hashed using Werkzeugs `generate_password_hash` before being stored. The used token is deleted with `delete_reset_token` to prevent reuse. If STMP is not configured or sending fails, the reset link is printed in the terminal for local testing.