from datetime import datetime

class Expense:

    def __init__(self, name, category, amount, date = None) -> None:
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, ${self.amount:.2f}, {self.date} >"