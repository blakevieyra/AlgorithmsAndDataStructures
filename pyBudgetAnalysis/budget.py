class Budget:

  def __init__(self, income):
    self.income = income

  def get_income(self):
    return f"${self.income}"

  def deduct_expenses(self, expense):
    self.income -= expense
    return f"{expense} has been deducted. Remaining balance: {self.income}"
