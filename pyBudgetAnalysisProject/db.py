import sqlite3

# Connect to a database (or create it if it doesn't exist)
conn = sqlite3.connect('budget_app.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create Users table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, username TEXT UNIQUE, password_hash TEXT, other_details TEXT)''')

# Create Expenses table
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (expense_id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, category TEXT, amount REAL,
                 FOREIGN KEY(user_id) REFERENCES users(user_id))''')

# Create Income table
cursor.execute('''CREATE TABLE IF NOT EXISTS income
                 (income_id INTEGER PRIMARY KEY, user_id INTEGER, date TEXT, amount REAL,
                 FOREIGN KEY(user_id) REFERENCES users(user_id))''')

# Save (commit) the changes
conn.commit()

# Close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
