import sqlite3

conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        is_logged_in BOOLEAN DEFAULT 0
    )
""")
conn.commit()
conn.close()
