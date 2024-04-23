import io
import matplotlib.pyplot as plt
from flask import session, flash, redirect, url_for, send_file

class Piechart:
    def __init__(self, expenses):
        self.expenses = expenses

    def display_pie_chart(self):
        if not self.expenses or sum(expense['amount'] for expense in self.expenses) <= 0:
            print("Invalid sizes: Sum must be greater than zero to plot a pie chart.")
            return None

        labels = [f"{expense['category']} - ${expense['amount']}" for expense in self.expenses]
        sizes = [expense['amount'] for expense in self.expenses]
        total_expenses = sum(sizes)

        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lavender']
        explode = (0.1,) + (0,) * (len(labels) - 1)

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, shadow=True, pctdistance=0.85)
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.axis('equal')
        plt.title(f'My Monthly Budget - Total Expenses: ${total_expenses:.2f}')
        plt.tight_layout()

        # Instead of showing the plot, return the figure
        return plt.gcf()