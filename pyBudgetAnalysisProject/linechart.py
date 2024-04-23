import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

class LineChart:
    def __init__(self):
        self.dates = []
        self.expenses = []

    def add_expense(self, date_str, amount):
        """Adds an expense to the chart.
        
        Args:
            date_str (str): The date of the expense in 'YYYY-MM-DD' format.
            amount (float): The amount of the expense.
        """
        date = datetime.strptime(date_str, '%Y-%m-%d')
        self.dates.append(date)
        self.expenses.append(amount)

    def plot(self):
        """Plots the line chart with the collected expense data."""
        plt.figure(figsize=(10, 5))
        plt.plot(self.dates, self.expenses, marker='o', linestyle='-')

        # Formatting the plot
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # every month
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # month and year
        plt.gca().xaxis.set_minor_locator(mdates.DayLocator())  # every day
        plt.gcf().autofmt_xdate()  # Rotation

        plt.title('Expense Tracking Over Time')
        plt.xlabel('Date')
        plt.ylabel('Expense Amount ($)')
        plt.grid(True)
        plt.show()

# Example usage
chart = LineChart()
chart.add_expense('2024-01-01', 100)
chart.add_expense('2024-02-15', 150)
chart.add_expense('2024-03-10', 200)
chart.plot()
