class Expenses:

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

  def get_bills(self):
    return self.bills

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

  def get_total_expenses(self):
    total_expenses = 0
    for k, v in self.bills.items():
      total_expenses += v
    return total_expenses
