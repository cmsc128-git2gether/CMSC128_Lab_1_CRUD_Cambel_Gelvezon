DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
<<<<<<< HEAD
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    due_date TEXT,
    due_time TEXT,
    priority TEXT CHECK (priority IN ('Low', 'Med', 'High')),
    tag TEXT CHECK (tag IN ('School', 'Personal', 'Others')),
    completed INTEGER NOT NULL DEFAULT 0,
    deleted INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
=======
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    due_date DATE,
    due_time TIME,
    priority VARCHAR(10),
    tag VARCHAR(20),
    completed TINYINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CHECK (priority IN ('Low', 'Med', 'High')),
    CHECK (tag IN ('School', 'Personal', 'Others'))
>>>>>>> gelvezon-mtfs
);