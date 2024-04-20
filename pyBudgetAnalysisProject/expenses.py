class Expenses:

  # Initialized expenses with monthly income and create dictionary with categories and their dollar values
  def __init__(self, income):
    self.income = income
    self.bills = {
        "Rent/Mortgage": 0,
        "Electricity": 0,
        "Water": 0,
        "Internet": 0,
        "Phone": 0,
        "Gas": 0,
        "Cable": 0,
        "Car": 0,
        "Insurance": 0,
        "Subscriptions": 0,
        "Credit Cards": 0,
        "Groceries": 0,
        "Dining Out": 0,
        "Entertainment": 0,
        "Savings": 0
    }
    
  # Getter for dictionary with categories and their dollar values
  def get_bills(self):
    return self.bills

  # Allow user to input dollar vale for eack category in the dictionary. Checks for valid input first and while valid, continues to the categories are assigned an expense
  def create_bills(self):
    print("Please enter dollar amounts for the following categories:\n")
    for key in self.bills:
      valid_input = False
      while not valid_input:
        try:
          self.bills[key] = int(input(f" {key}: "))
          valid_input = True
        except ValueError:
          print("Please enter a valid number for expense.")
    return self.bills

  # Getter for expenses per the dictionary. Add the values from the bills dictionary and return the total expense amount
  def get_total_expenses(self):
    total_expenses = 0
    for k, v in self.bills.items():
      total_expenses += v
    return total_expenses
