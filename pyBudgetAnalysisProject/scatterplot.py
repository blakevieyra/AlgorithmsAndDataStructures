import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

class ScatterPlot:
    def __init__(self):
        self.dates = []
        self.incomes = []

    def add_income(self, date_str, amount):
        """Adds an income entry to the dataset."""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        self.dates.append(date)
        self.incomes.append(amount)

    def plot(self):
        """Plots the scatter plot with the collected income data."""
        plt.figure(figsize=(10, 5))
        scatter = plt.scatter(self.dates, self.incomes, color='blue', marker='o')

        # Formatting the plot
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
        plt.gcf().autofmt_xdate()  # Rotation

        # Annotating each data point
        for i, (date, income) in enumerate(zip(self.dates, self.incomes)):
            plt.annotate(f"{date.strftime('%Y-%m-%d')}", (mdates.date2num(date), income), 
                         textcoords="offset points", xytext=(0,10), ha='center')

        plt.title('Income Tracking Over Time')
        plt.xlabel('Date')
        plt.ylabel('Income Amount ($)')
        plt.grid(True)
        plt.show()

# Example usage in your Flask route
