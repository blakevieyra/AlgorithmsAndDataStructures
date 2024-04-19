import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class Histogram:

  def __init__(self, expenses):
    if not expenses:
      raise ValueError("Expenses data is required to create a histogram.")
    self.expenses = expenses

  def display_histogram(self):
    categories = list(self.expenses.keys())
    amounts = list(self.expenses.values())
    total_expenses = sum(amounts)  # Calculate total expenses

    colors = cm.get_cmap('viridis')(np.linspace(
        0, 1, len(categories)))  # Use a colormap for varied colors

    fig, ax = plt.subplots(
        figsize=(10, 8))  # Create a figure and a set of subplots
    bars = ax.bar(categories, amounts, color=colors)

    ax.set_xlabel('Expense Categories', fontsize=12)
    ax.set_ylabel('Amount ($)', fontsize=12)
    ax.set_title(f'My Monthly Budget - Total Expenses: ${total_expenses:.2f}',
                 fontsize=14)
    ax.set_xticks(range(
        len(categories)))  # Set the x-ticks to match the categories
    ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=10)

    # Annotate each bar with the amount
    for bar in bars:
      yval = bar.get_height()
      ax.text(
          bar.get_x() + bar.get_width() / 2,
          yval,
          f'${yval:.2f}',
          va='bottom',  # Vertical alignment
          ha='center',
          fontsize=9,
          color='black')

    plt.tight_layout(
    )  # Adjust the plot to make room for the rotated x-axis labels
    plt.show()
