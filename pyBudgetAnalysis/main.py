import expenses as exp
import budget as bud
import piechart as pch
import histogram as his
import csv
from datetime import datetime
import numpy as np
import sys

class Main:
    def __init__(self):
        self.name = input("Please enter your first name: ")
        self.income = self.get_valid_income()
        self.bill_account = exp.Expenses(self.income)
        self.cli_menu()

    def cli_menu(self):
        menu_options = {
            "1": "Manage monthly expenses",
            "2": "Change monthly income",
            "3": "View budget",
            "4": "Generate spreadsheet",
            "5": "Receive Budget Analysis",
            "6": "Exit"
        }
        while True:
            print("\n--- Main Menu ---")
            for key in sorted(menu_options.keys()):
                print(f"{key}: {menu_options[key]}")
            selection = input("Please select an option: ")
            if selection == '1':
                self.manage_expenses()
            elif selection == '2':
                self.reset_income()
            elif selection == '3':
                print(f"\n--{self.name}'s Budget--")
                self.manage_budget()
            elif selection == '4':
                self.write_to_csv()
                print("Spreadsheet generated.")
            elif selection == '5':
                self.display_budget_analysis()
                self.visualize_data()
                print("Budget analysis displayed.")
                print("Report generated.")
            elif selection == '6':
                print('Exiting program. Goodbye!')
                sys.exit()
            else:
                print("Invalid selection, please try again.")
    
    def reset_income(self):
        self.income = self.get_valid_income()

    def get_valid_income(self):
        while True:
            try:
                income = float(input("Please enter your monthly income: "))
                if income >= 0:
                    return income
                else:
                    print("Please enter a number greater than zero.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def manage_expenses(self):
        self.bill_account.create_bills()
        for category, amount in self.bill_account.get_bills().items():
            print(f"{category}: ${amount}")
        print("Total Expenses: $" + str(self.bill_account.get_total_expenses()))

    def manage_budget(self):
        self.budget = bud.Budget(self.income)
        print("Monthly Income: " + str(self.budget.get_income()))
        print("Monthly Expenses: $" + str(self.bill_account.get_total_expenses()))
        remaining_balance = self.income - self.bill_account.get_total_expenses()
        print("Remaining Balance: $" + str(remaining_balance))

    def visualize_data(self):
        chart = pch.Piechart(self.bill_account.get_bills())
        chart.display_pie_chart()
        histogram = his.Histogram(self.bill_account.get_bills())
        histogram.display_histogram()

    def write_to_csv(self):
        with open('spendingtracker.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Expense Category', 'Amount'])
            for category, amount in self.bill_account.get_bills().items():
                writer.writerow([category, amount])
            total_expenses = self.bill_account.get_total_expenses()
            remainder = self.income - total_expenses
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(['Total Expenses', 'Income', 'Remaining Balance', 'Date'])
            writer.writerow([total_expenses, self.income, remainder, current_date])

    def display_budget_analysis(self):
        print('\n--Budget Analysis--')
        analysis = self.run_statistics()
        print("\n".join(analysis))

    def run_statistics(self):
        bills = self.bill_account.get_bills()
        if not bills:
            return ["No expense data available."]
        expense_values = list(bills.values())
        expense_categories = list(bills.keys())
        max_expense = max(expense_values) if expense_values else 0
        min_expense = min(expense_values) if expense_values else 0
        max_category = expense_categories[expense_values.index(max_expense)] if max_expense > 0 else "None"
        min_category = expense_categories[expense_values.index(min_expense)] if min_expense > 0 else "None"
        avg_expense = np.mean(expense_values) if expense_values else 0
        std_deviation = np.std(expense_values) if expense_values else 0
        cv = (std_deviation / avg_expense * 100) if avg_expense else 0
        analysis = self.budget_analysis(max_expense, avg_expense, std_deviation, cv)
        return [
            f"Max Expense: ${max_expense} ({max_category})",
            f"Min Expense: ${min_expense} ({min_category})",
            f"Avg Expense: ${avg_expense:.2f}",
            f"Standard Deviation: {std_deviation:.2f}",
            f"Coefficient of Variation: {cv:.2f}%",
            analysis
        ]

    def budget_analysis(self, max_expense, avg_expense, std_deviation, cv):
        analysis_message = []
        if not hasattr(self, 'income') or self.income <= 0:
            analysis_message.append("Income is zero or not set, unable to compare expenses to income.")
            self.write_analysis_to_file(analysis_message)
            return

        if cv > 50:
            analysis_message.append("High variability in expenses. Consider stabilizing spending.")
        else:
            analysis_message.append("Expenses are relatively stable. Keep tracking to maintain budget health.")

        if std_deviation > 0.5 * avg_expense:
            analysis_message.append("Your expenses show significant month-to-month variation.")
        else:
            analysis_message.append("Your month-to-month expenses are fairly consistent.")

        if max_expense > 2 * avg_expense:
            analysis_message.append("Your highest expense is significantly higher than your average expenses. Review if such high expenses are necessary or can be reduced.")
        else:
            analysis_message.append("Your highest expense is within a normal range compared to your average expenses.")

        if max_expense > 0.4 * self.income:
            analysis_message.append("Warning: Your highest single expense constitutes a large portion of your income. Ensure this is sustainable.")

        total_expenses = sum(self.bill_account.get_bills().values())
        for category, amount in self.bill_account.get_bills().items():
            percentage_of_total = (amount / total_expenses) * 100
            percentage_of_income = (amount / self.income) * 100
            if percentage_of_total > 15:
                analysis_message.append(f"Consider reducing {category}, which accounts for {percentage_of_total:.2f}% of your total expenses.")
            if percentage_of_income > 10:
                analysis_message.append(f"Alert: {category} expenses take up more than 10% of your income. Consider budget adjustments.")

        self.write_analysis_to_file(analysis_message)
        return "\n".join(analysis_message)

    def write_analysis_to_file(self, analysis_message):
        with open('budget_analysis.txt', 'w') as file:
            file.write("Budget Analysis Report\n")
            file.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for line in analysis_message:
                file.write(line + "\n")

if __name__ == "__main__":
    main = Main()
