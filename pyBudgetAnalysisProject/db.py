import sqlite3

conn = sqlite3.connect('budget_app.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT,
        other_details TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date TEXT,
        category TEXT,
        amount REAL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
        income_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date TEXT,
        amount REAL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
''')

conn.commit()

conn.close()
