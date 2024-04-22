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
import matplotlib
from main import run_statistics, write_to_csv

matplotlib.use('Agg')  # Use a non-GUI backend to prevent chart popups

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

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
            session['user_id'] = user['id']
            cursor.execute("SELECT amount FROM income WHERE user_id = ?", (user['id'],))
            income = cursor.fetchone()
            if income:
                session['income'] = income['amount']
                
            return redirect(url_for('manage_expenses'))
        else:
            flash('Invalid username or password.', 'error')
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
                    

@app.route('/set_income', methods=['POST'])
def set_income():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to continue.', 'error')
        return redirect(url_for('login'))

    try:
        income = float(request.form.get('income', 0))  # Default to 0 if not provided
        if income <= 0:
            raise ValueError("Income must be a positive number.")

        db = get_db()
        cursor = db.cursor()
        current_date = datetime.now().strftime('%Y-%m-%d')
        # Consider using an UPDATE statement if only keeping track of the latest income
        cursor.execute('''
            INSERT INTO income (user_id, date, amount)
            VALUES (?, ?, ?) ON CONFLICT(user_id) DO UPDATE SET amount = excluded.amount;
        ''', (user_id, current_date, income))
        db.commit()
        flash('Income updated successfully!', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    except Exception as e:
        flash('Failed to update income due to a system error.', 'error')
    finally:
        if db:
            db.close()

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
        user_id = session.get('user_id')
        if not user_id:
            flash('User not logged in.')
            return redirect(url_for('login'))

        db = get_db()
        cursor = db.cursor()

        # Retrieve expenses data from the database using the user ID
        cursor.execute('SELECT category, amount FROM expenses WHERE user_id = ?', (user_id,))
        expenses_data = cursor.fetchall()

        # Generate the CSV content
        csv_content = "Category,Amount\n"
        for expense in expenses_data:
            csv_content += f"{expense['category']},{expense['amount']}\n"

        # Close the database connection
        cursor.close()
        db.close()

        # Send the generated CSV file as a response
        response = make_response(csv_content)
        response.headers['Content-Disposition'] = 'attachment; filename=spendingtracker.csv'
        response.mimetype = 'text/csv'
        return response
    except Exception as e:
        flash(f"Error generating spreadsheet: {str(e)}")
        return redirect(url_for('index'))
    

@app.route('/histogram')
def histogram():
    user_id = session.get('user_id')
    if not user_id:
        flash('User not logged in.')
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()

    try:
        # Retrieve expenses for the user from the database
        cursor.execute('SELECT category, amount FROM expenses WHERE user_id = ?', (user_id,))
        expenses = cursor.fetchall()

        if not expenses:
            flash('No expenses found for the user.')
            return redirect(url_for('budget_analysis'))

        buf = io.BytesIO()
        Histogram(expenses).display_histogram()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=False)
    except Exception as e:
        flash(f"Error generating histogram: {str(e)}")
        return redirect(url_for('budget_analysis'))
    finally:
        cursor.close()
        db.close()

@app.route('/piechart')
def piechart():
    user_id = session.get('user_id')
    if not user_id:
        flash('User not logged in.')
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()

    try:
        # Retrieve expenses for the user from the database
        cursor.execute('SELECT category, amount FROM expenses WHERE user_id = ?', (user_id,))
        expenses = cursor.fetchall()

        if not expenses:
            flash('No expenses found for the user.')
            return redirect(url_for('budget_analysis'))

        buf = io.BytesIO()
        Piechart(expenses).display_pie_chart()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return send_file(buf, mimetype='image/png', as_attachment=False)
    except Exception as e:
        flash(f"Error generating pie chart: {str(e)}")
        return redirect(url_for('budget_analysis'))
    finally:
        cursor.close()
        db.close()

@app.route('/budget_analysis')
def budget_analysis():
    user_id = session.get('user_id')
    if not user_id:
        flash('User not logged in.')
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor()

    budget_data = {'income': 0, 'expenses': 0}  # Default empty data
    expenses = []
    balance = 0
    analysis_results = []

    try:
        cursor.execute('SELECT income, expenses FROM budget WHERE user_id = ?', (user_id,))
        budget = cursor.fetchone()

        if budget:
            budget_data = budget
            balance = budget['income'] - budget['expenses']

        cursor.execute('SELECT category, amount FROM expenses WHERE user_id = ? ORDER BY amount DESC', (user_id,))
        expenses = cursor.fetchall()

        # Here you should handle if no analysis results exist:
        analysis_results = run_statistics() if run_statistics() else ["No detailed analysis data available."]

    except Exception as e:
        flash(f"Error during analysis: {e}")

    finally:
        cursor.close()
        db.close()

    return render_template('budget_analysis.html', budget=budget_data, balance=balance, expenses=expenses, analysis=analysis_results)

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

        # Calculate the expense ratio and determine the grade
        if income > 0:
            expense_ratio = (expenses / income) * 100
        else:
            expense_ratio = 0  # Avoid division by zero

        # Define the grading logic
        if expense_ratio <= 50:
            grade = 'A+'
        elif expense_ratio <= 70:
            grade = 'A'
        elif expense_ratio <= 90:
            grade = 'A-'
        elif expense_ratio <= 110:
            grade = 'B'
        elif expense_ratio <= 130:
            grade = 'C'
        elif expense_ratio <= 150:
            grade = 'D'
        else:
            grade = 'F-'

        # Include grade in the budget data dictionary
        budget_data = {
            'income': income,
            'expenses': expenses,
            'balance': balance,
            'grade': grade  # Include the grade in the budget data sent to the template
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

    # Fetch existing expenses to display and potentially update
    cursor.execute('SELECT category, amount FROM expenses WHERE user_id = ?', (user_id,))
    categories_with_amounts = {row['category']: row['amount'] for row in cursor.fetchall()}

    if request.method == 'POST':
        # Get data from the form
        categories_post = request.form.getlist('categories[]')
        amounts_post = request.form.getlist('amounts[]')

        # Convert amounts to float and prepare data for insertion or update
        try:
            updated_data = [(user_id, category, float(amount)) for category, amount in zip(categories_post, amounts_post)]
            for data in updated_data:
                cursor.execute('''
                    INSERT INTO expenses (user_id, category, amount)
                    VALUES (?, ?, ?)
                    ON CONFLICT(user_id, category)
                    DO UPDATE SET amount = excluded.amount;
                ''', data)
            db.commit()
            update_budget(user_id)
            flash('Expenses updated successfully!')
            # Update the local dictionary to reflect the new amounts immediately after saving
            categories_with_amounts = {data[1]: data[2] for data in updated_data}
        except Exception as e:
            db.rollback()
            flash(f"An error occurred while updating expenses: {e}")

        # Redirect to clear POST data and refresh the page
        return redirect(url_for('manage_expenses'))

    # Calculate total expenses for display
    total_expenses = sum(categories_with_amounts.values())

    cursor.close()
    db.close()

    return render_template('manage_expenses.html', categories=categories_with_amounts, total_expenses=total_expenses)

@app.route('/save_expenses', methods=['POST'])
def save_expenses():
    user_id = session.get('user_id')
    if not user_id:
        flash('User not logged in. Please login to continue.', 'error')
        return redirect(url_for('login'))

    try:
        db = get_db()
        cursor = db.cursor()

        # Assuming you're sending categories and amounts as lists from the form
        categories = request.form.getlist('categories[]')
        amounts = request.form.getlist('amounts[]')

        if not categories or not amounts:
            flash('No expenses data provided.', 'error')
            return redirect(url_for('manage_expenses'))

        for category, amount in zip(categories, map(float, amounts)):
            cursor.execute('''
                INSERT INTO expenses (user_id, category, amount, date)
                VALUES (?, ?, ?, DATE('now'))
                ''', (user_id, category, amount))
        db.commit()
        update_budget(user_id)
        flash('Expenses saved successfully!', 'success')

    except sqlite3.IntegrityError:
        db.rollback()
        flash('Database error occurred. Try again.', 'error')
    except ValueError:
        db.rollback()
        flash('Invalid amount entered. Please enter a valid number.', 'error')
    finally:
        cursor.close()
    return redirect(url_for('budget_analysis'))

def update_budget(user_id):
    db = get_db()
    cursor = db.cursor()

    try:
        # Calculate total expenses
        cursor.execute('SELECT SUM(amount) AS total_expenses FROM expenses WHERE user_id = ?', (user_id,))
        total_expenses = cursor.fetchone()['total_expenses'] or 0

        # Fetch current income
        cursor.execute('SELECT amount FROM income WHERE user_id = ?', (user_id,))
        current_income = cursor.fetchone()['amount'] or 0

        # Calculate new budget or available income
        new_available_income = current_income - total_expenses

        # Update the income table or a budget table if exists
        cursor.execute('UPDATE income SET amount = ? WHERE user_id = ?', (new_available_income, user_id))
        db.commit()
        flash('Budget updated successfully!', 'success')
    except Exception as e:
        db.rollback()
        flash(f"An error occurred while recalculating the budget: {e}", 'error')
    finally:
        cursor.close()
        db.close()
        
if __name__ == '__main__':
    app.run(debug=True)