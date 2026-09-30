DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

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
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    due_date DATE,
    due_time TIME,
    priority VARCHAR(10),
    tag VARCHAR(20),
    completed TINYINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CHECK (priority IN ('Low', 'Med', 'High')),
    CHECK (tag IN ('School', 'Personal', 'Others'))
<<<<<<< HEAD
>>>>>>> gelvezon-mtfs
);
=======
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

>>>>>>> origin/act2-accounts-emg
