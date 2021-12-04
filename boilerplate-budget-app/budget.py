import math

class Category:
  def __init__(self, name):
    self.ledger = []
    self.name = name
    self.balance = 0

  def __str__(self):
    width = 30
    filler = "*"
    descWidth = 23
    amountWidth = 7

    nameLen = len(self.name)
    leftLen = math.floor((width-nameLen)/2)
    rightLen = width - nameLen - leftLen

    outputStr = f'{"" :{filler}<{leftLen}}{self.name}{"" :{filler}<{rightLen}}\n'
    filler = " "
    for entry in self.ledger:
      descStr = entry["description"][:descWidth]
      amountStr = f'{entry["amount"]:.2f}'
      outputStr = outputStr + f'{descStr:{filler}<{descWidth}}{amountStr:{filler}>{amountWidth}}\n'
    outputStr = outputStr + f'Total: {self.balance}'

    return outputStr

  def deposit(self, amount, description=""):
    self.balance = self.balance + amount
    if self.ledger is None:
      self.ledger = []
  
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      self.balance = self.balance - amount
      self.ledger.append({"amount": -amount, "description": description})
      return True
    else:
      return False

  def get_balance(self):
    return self.balance

  def transfer(self, amount, anotherCategory):
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to {anotherCategory.name}")
      anotherCategory.deposit(amount, f"Transfer from {self.name}")
      return True
    else:
      return False

  def check_funds(self, amount):
    if abs(amount) > self.balance:
      return False
    else:
      return True


def create_spend_chart(categories):
  #
  # Extract the withdrawal entries
  #
  catExpenses = []
  total = 0
  for category in categories:
    catExpense = 0
    catName = category.name
    for entry in category.ledger:
      if entry["amount"] < 0:
        catExpense = catExpense + abs(entry["amount"])
    catExpenses.append({"name": catName, "amount": catExpense})
    total = total + catExpense

  #
  # Calculate the withdrawal percentage
  #
  for i in range(len(catExpenses)):
    expense = catExpenses[i]
    percentage = expense["amount"] / total * 100
    percentage = int(math.floor(percentage / 10.0)) * 10
    expense["percentage"] = percentage
    catExpenses[i] = expense

  #
  # Draw the bar char
  #
  filler = " "
  maxNameLen = 0
  chartStr = "Percentage spent by category\n"
  for i in range(100, -1, -10):
    percentage = str(i)
    chartStr = chartStr + f'{percentage :{filler}>3}|'
    for expense in catExpenses:
      if len(expense["name"]) > maxNameLen:
        maxNameLen = len(expense["name"])
      if expense["percentage"] >= i:
        chartStr = chartStr + " o "
      else:
        chartStr = chartStr + "   "
    chartStr = chartStr + " \n"

  # Print x-axis
  filler = "-"
  x = len(catExpenses)*3 + 5
  chartStr = chartStr + f'{"    " :{filler}<{x}}'
  
  # Print name
  for i in range(maxNameLen):
    chartStr = chartStr + "\n     "
    for expense in catExpenses:
      if len(expense["name"])> i:
        chartStr = chartStr + f'{expense["name"][i]}  '
      else:
        chartStr = chartStr + "   "

  return chartStr