import matplotlib.pyplot as plt

class Piechart:
  
  # Initializes the piechart class with user provided expense data
  def __init__(self, expenses):
    self.expenses = expenses
  
  # Check if there are any expenses to plots by summing the values and ensure size greater than zero
  def display_pie_chart(self):
      if not self.expenses or sum(self.expenses.values()) <= 0:
          print("Invalid sizes: Sum must be greater than zero to plot a pie chart.")
          return  

      # Creates a list of piechart labels and sizes fpr key and values in expenses. Then calculate total sum expenses
      labels = [f'{key} - ${value}' for key, value in self.expenses.items()]
      sizes = list(self.expenses.values())
      total_expenses = sum(sizes)  

      # Sets color for piechart for visual appeal and explodes a section of the chart for visual appeal 
      colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lavender']
      explode = (0.1,) + (0,) * (len(labels) - 1)  

      # Plots the pie chart, setting size, labels, colors, and a visually applealing design
      plt.figure(figsize=(8, 6))
      plt.pie(sizes,
              explode=explode,
              labels=labels,
              colors=colors,
              autopct=lambda pct: f'{pct:.1f}%',
              startangle=140,
              shadow=True,
              pctdistance=0.85)

      # Adding a circle at the center to turn the pie for visual appeal
      centre_circle = plt.Circle((0, 0), 0.70, fc='white')
      fig = plt.gcf()
      fig.gca().add_artist(centre_circle)

      # Ensure size of pie is correct and add the Title to the chart
      plt.axis('equal')
      plt.title(f'My Monthly Budget - Total Expenses: ${total_expenses:.2f}')
      plt.show()
