import matplotlib.pyplot as plt

class Piechart:
  
  def __init__(self, expenses):
    if not expenses:
      raise ValueError("Expenses data is required to create a piechart.")
    self.expenses = expenses
  
  def display_pie_chart(self):
      # Check if there are any expenses to plot
      if not self.expenses or sum(self.expenses.values()) <= 0:
          print("Invalid sizes: Sum must be greater than zero to plot a pie chart.")
          return  # Exit the function if there are no valid expenses to display

      # Preparing data for the pie chart
      labels = [f'{key} - ${value}' for key, value in self.expenses.items()]
      sizes = list(self.expenses.values())
      total_expenses = sum(sizes)  # This should now be calculated correctly before plotting

      # Setting colors and explode parameters for the pie chart
      colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lavender']
      explode = (0.1,) + (0,) * (len(labels) - 1)  # Safely create explode tuple

      # Plotting the pie chart
      plt.figure(figsize=(8, 6))
      plt.pie(sizes,
              explode=explode,
              labels=labels,
              colors=colors,
              autopct=lambda pct: f'{pct:.1f}%',
              startangle=140,
              shadow=True,
              pctdistance=0.85)

      # Adding a circle at the center to turn the pie into a donut chart
      centre_circle = plt.Circle((0, 0), 0.70, fc='white')
      fig = plt.gcf()
      fig.gca().add_artist(centre_circle)

      # Ensuring the pie chart is drawn as a circle
      plt.axis('equal')
      plt.title(f'My Monthly Budget - Total Expenses: ${total_expenses:.2f}')
      plt.show()
