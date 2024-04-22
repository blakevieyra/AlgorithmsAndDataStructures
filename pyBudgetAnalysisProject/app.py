from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask import send_file, make_response
import sqlite3
import bcrypt
import secrets
import io
from matplotlib import pyplot as plt
from histogram import Histogram
from main import Main
from piechart import Piechart
from datetime import datetime


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
main_app = Main("User", 0)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('budget_app.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html', name="Home Page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            session['logged_in'] = True
            session['user_id'] = user['id']  # Store user ID in session
            return redirect(url_for('manage_expenses'))
        else:
            return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        db = get_db()
        cursor = db.cursor()

        # Ensure the users table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT
            )
        """)

        # Check if username already exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            db.close()
            flash('Username already exists. Please choose another username.')
            return redirect(url_for('register'))

        # Insert the new user
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        user_id = cursor.lastrowid  # Get the last inserted id

        # Initialize the income table with default value of 0 for new users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS income (
                income_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                date TEXT,
                amount REAL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        cursor.execute("INSERT INTO income (user_id, date, amount) VALUES (?, ?, ?)", (user_id, datetime.now().strftime("%Y-%m-%d"), 0.0))

        # Ensure the expenses table exists and initialize default categories
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                expense_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                date TEXT,
                category TEXT,
                amount REAL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        """)
        default_categories = [
            "Housing", "Electricity", "Water", "Internet", "Phone", "Gas", 
            "Cable", "Car", "Insurance", "Subscriptions", "Credit Cards", "Groceries", 
            "Dining Out", "Entertainment", "Savings", "Loan Payments", "Etc"
        ]
        default_expenses = [(user_id, datetime.now().strftime("%Y-%m-%d"), category, 0.0) for category in default_categories]
        cursor.executemany("INSERT INTO expenses (user_id, date, category, amount) VALUES (?, ?, ?, ?)", default_expenses)

        db.commit()
        db.close()
        flash('Account created successfully! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clears all data in session, effectively logging out the user
    flash('You have been logged out successfully.')
    return redirect(url_for('index'))

from datetime import datetime

@app.route('/set_income', methods=['POST'])
def set_income():
    user_id = session.get('user_id')
    income = request.form.get('income', type=float)

    if income and income > 0:
        db = get_db()
        cursor = db.cursor()
        current_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO income (user_id, date, amount)
            VALUES (?, ?, ?);
            ''', (user_id, current_date, income))
        db.commit()
        db.close()
        flash('Income updated successfully!')
    else:
        flash('Invalid input. Please enter a valid positive number.')

    return redirect(url_for('index'))

@app.route('/download')
def download_file():
    content = "Some content"
    response = make_response(content)
    response.headers['Content-Disposition'] = 'attachment; filename=filename.txt'
    response.mimetype = 'text/plain'
    return response

@app.route('/generate_spreadsheet')
def generate_spreadsheet():
    try:
        filename = 'spendingtracker.csv'
        main_app.write_to_csv(filename)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        flash(f"Error generating spreadsheet: {str(e)}")
        return redirect(url_for('index'))

@app.route('/budget_analysis')
def budget_analysis():
    try:
        analysis_results = main_app.run_statistics()
        if analysis_results:
            return render_template('budget_analysis.html', analysis=analysis_results)
        else:
            flash("No expense data available for analysis.")
            return redirect(url_for('manage_expenses'))
    except Exception as e:
        flash(f"Error generating analysis: {e}")
        return redirect(url_for('index'))


@app.route('/histogram')
def histogram():
    buf = io.BytesIO()
    expenses = main_app.bill_account.get_bills()
    Histogram(expenses).display_histogram()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/piechart')
def piechart():
    buf = io.BytesIO()
    expenses = main_app.bill_account.get_bills()
    Piechart(expenses).display_pie_chart()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/save_expenses', methods=['POST'])
def save_expenses():
    user_id = session.get('user_id')  # Assuming user ID is stored in the session
    if not user_id:
        return "User not logged in", 401  # Unauthorized

    expenses = request.json
    db = get_db()
    cursor = db.cursor()
    try:
        for category, amount in expenses.items():
            cursor.execute("INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)", (user_id, category, amount))
        db.commit()
        return "Expenses saved successfully!", 200
    except Exception as e:
        db.rollback()
        return f"An error occurred: {str(e)}", 500
    finally:
        cursor.close()
        db.close()


@app.route('/view_budget')
def view_budget():
    user_id = session.get('user_id')  # Assuming user_id is stored in the session upon login
    
    if user_id:
        db = get_db()
        cursor = db.cursor()

        # Fetch the latest income for the user
        cursor.execute('SELECT amount FROM income WHERE user_id = ? ORDER BY date DESC LIMIT 1', (user_id,))
        income_row = cursor.fetchone()
        income = income_row['amount'] if income_row else 0.0

        # Fetch the total expenses for the user
        cursor.execute('SELECT SUM(amount) AS total_expenses FROM expenses WHERE user_id = ?', (user_id,))
        expenses_row = cursor.fetchone()
        expenses = expenses_row['total_expenses'] if expenses_row else 0.0

        db.close()

        # Calculate the overall balance
        balance = income - expenses

        budget_data = {
            'income': income,
            'expenses': expenses,
            'balance': balance
        }

        return render_template('view_budget.html', budget=budget_data)
    else:
        flash('User not logged in.')
        return redirect(url_for('login'))

@app.route('/generate_report')
def generate_report():
    try:
        report_filename = 'budget_analysis.txt'
        main_app.write_analysis_to_file(report_filename)
        return send_file(report_filename, as_attachment=True)
    except Exception as e:
        flash(f"Error generating report: {e}")
        return redirect(url_for('index'))

@app.route('/manage_expenses', methods=['GET', 'POST'])
def manage_expenses():
    user_id = session.get('user_id')
    if not user_id:
        flash('User not logged in.')
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT DISTINCT category FROM expenses WHERE user_id = ?', (user_id,))
    categories = [row['category'] for row in cursor.fetchall()]

    if request.method == 'POST':
        categories_post = request.form.getlist('categories[]')
        amounts_post = request.form.getlist('amounts[]')

        try:
            for category, amount in zip(categories_post, map(float, amounts_post)):
                cursor.execute('''
                    INSERT INTO expenses (user_id, category, amount)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id, category)
                    DO UPDATE SET amount = excluded.amount;
                ''', (user_id, category, amount))
            db.commit()
            flash('Expenses updated successfully!')
        except Exception as e:
            db.rollback()
            flash(f"An error occurred while updating expenses: {str(e)}")
        finally:
            cursor.close()
        return redirect(url_for('manage_expenses'))

    # Handling GET request or following the POST redirect
    cursor = db.cursor()  # Necessary to reinitialize the cursor after it's closed
    cursor.execute('SELECT category, sum(amount) as total_amount FROM expenses WHERE user_id = ? GROUP BY category', (user_id,))
    expenses_data = cursor.fetchall()
    db.close()  # Close the database after completing the queries

    categories_with_amounts = {exp['category']: exp['total_amount'] for exp in expenses_data if expenses_data}
    total_expenses = sum(exp['total_amount'] for exp in expenses_data) if expenses_data else 0.0

    return render_template('manage_expenses.html', categories=categories_with_amounts, total_expenses=total_expenses)

if __name__ == '__main__':
    app.run(debug=True)