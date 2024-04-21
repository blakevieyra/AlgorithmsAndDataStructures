from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from main import Main  # Make sure the Main class is adapted to work with Flask
from flask import send_file


app = Flask(__name__)
app.secret_key = 'your_secret_key'

main_app = Main("Web User", 1000)  # Initialized with default values

@app.route('/')
def index():
    return render_template('index.html', name="User's Name")

@app.route('/set_income', methods=['POST'])
def set_income():
    try:
        income = float(request.form['income'])
        if income > 0:
            main_app.set_income(income)  # use the method in Main class
            flash('Income updated successfully!')
        else:
            flash('Please enter a positive number for income.')
    except ValueError:
        flash('Invalid input. Please enter a valid number.')
    return redirect(url_for('index'))

@app.route('/manage_expenses', methods=['GET', 'POST'])
def manage_expenses():
    if request.method == 'POST':
        category = request.form.get('category')
        amount = request.form.get('amount', type=float)
        if category and amount:
            main_app.add_expense(category, amount)
            flash('Expense added successfully!')
        else:
            flash('Please fill in all fields correctly.')

    categories = main_app.get_categories()  # This function needs to be defined to fetch existing categories
    expenses = main_app.get_expenses()
    total_expenses = main_app.total_expenses()
    return render_template('manage_expenses.html', categories=categories, expenses=expenses, total_expenses=total_expenses)

@app.route('/view_budget')
def view_budget():
    budget_data = {
        'income': main_app.income,
        'expenses': main_app.bill_account.get_total_expenses(),
        'balance': main_app.income - main_app.bill_account.get_total_expenses()
    }
    return render_template('view_budget.html', budget=budget_data)

@app.route('/generate_report')
def generate_report():
    try:
        report_filename = 'budget_analysis.txt'
        main_app.write_analysis_to_file(report_filename)
        return send_file(report_filename, as_attachment=True)
    except Exception as e:
        flash(f"Error generating report: {e}")
        return redirect(url_for('index'))
            
from flask import make_response

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
        filename = 'spendingtracker.csv'  # Define the filename
        main_app.write_to_csv(filename)   # Generate the CSV file
        return send_file(filename, as_attachment=True)  # Serve the file as an attachment
    except Exception as e:
        flash(f"Error generating spreadsheet: {str(e)}")
        return redirect(url_for('index'))

@app.route('/budget_analysis')
def budget_analysis():
    try:
        analysis_results = main_app.run_statistics()  # Run the analysis and fetch results
        if analysis_results:
            return render_template('budget_analysis.html', analysis=analysis_results)
        else:
            flash("No expense data available for analysis.")
            return redirect(url_for('manage_expenses'))
    except Exception as e:
        flash(f"Error generating analysis: {e}")
        return redirect(url_for('index'))


@app.route('/add_expense', methods=['POST'])
def add_expense():
    category = request.form.get('category')
    try:
        amount = float(request.form.get('amount'))
        if category and amount >= 0:
            main_app.bill_account.add_bill(category, amount)
            flash('Expense added successfully!')
        else:
            flash('Please fill in all fields correctly and ensure amount is non-negative.')
    except ValueError:
        flash('Invalid amount. Please enter a valid number.')
    return redirect(url_for('manage_expenses'))

if __name__ == '__main__':
    app.run(debug=True)
