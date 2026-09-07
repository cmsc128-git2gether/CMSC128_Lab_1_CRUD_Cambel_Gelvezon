DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    due_date TEXT,
    priority TEXT NOT NULL DEFAULT 'Low' CHECK (priority IN ('Low', 'Med', 'High')),
    tag TEXT NOT NULL DEFAULT 'Others' CHECK (tag IN ('School', 'Personal', 'Others')),
    completed INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);