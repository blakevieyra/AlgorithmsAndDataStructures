import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class Histogram:
    def __init__(self, expenses):
        if not expenses:
            raise ValueError("Expenses data is required to create a histogram.")
        self.expenses = {exp['category']: exp['amount'] for exp in expenses}

    def display_histogram(self):
        categories = list(self.expenses.keys())
        amounts = list(self.expenses.values())
        total_expenses = sum(amounts)
        colors = cm.get_cmap('viridis')(np.linspace(0, 1, len(categories)))
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.bar(categories, amounts, color=colors)
        ax.set_xlabel('Expense Categories', fontsize=12)
        ax.set_ylabel('Amount ($)', fontsize=12)
        ax.set_title(f'My Monthly Budget - Total Expenses: ${total_expenses:.2f}', fontsize=14)
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=10)
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval, f'${yval:.2f}', va='bottom', ha='center', fontsize=9, color='black')
        plt.tight_layout()
        return fig