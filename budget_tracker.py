from expense import Expense
import calendar
import datetime
from collections import defaultdict

def main():
    print(f"Running Budget Tracker")
    expenses_file_path = "budget.csv"
    budget = 500

    # Get user to input their expenses
    expense = get_user_expense()

    # Write the expenses to a file
    save_expense_to_file(expense, expenses_file_path)
    
    # Read file and summarize expenses
    summarize_expense(expenses_file_path, budget)

def get_user_expense():
    print(f"Getting the user expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "🍔 Food",
        "🚖 Transportation",
        "🛒 Groceries",
        "🪩 Fun",
        "😑 Miscellaneous"
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i + 1}. {category_name}")
        value_range = f"[1 - {len(expense_categories)}]"
        selected_category = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_category in range(len(expense_categories)):
            specific_category = expense_categories[selected_category]
            new_expense = Expense(
                name=expense_name, category=specific_category, amount=expense_amount
            )
            return new_expense
        else:
            print(f"Invalid category number. Please try again.")

def save_expense_to_file(expense: Expense, expenses_file_path):
    print(f"Saving user expense: {expense} to {expenses_file_path}")
    with open(expenses_file_path, "a") as f:
        f.write(f"{expense.date}, {expense.name}, {expense.amount}, {expense.category}\n")

def summarize_expense(expenses_file_path, budget):
    print(f"Summarizing user expense")
    expenses = []
    with open(expenses_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_date, expense_name, expense_amount, expense_category = line.strip().split(", ")
            line_expense = Expense(
                name = expense_name, 
                amount = float(expense_amount), 
                category = expense_category,
                date = expense_date
            )
            expenses.append(line_expense)
    
    expenses_by_month = defaultdict(list)
    for expense in expenses:
        month = expense.date[:7]
        expenses_by_month[month].append(expense)

    # Write summarized expenses to a new CSV file
    with open("summarized_budget.csv", "w") as f:
        for month, monthly_expenses in expenses_by_month.items():
            f.write(f"Month: {month}\n")
            f.write("Date, Name, Amount, Category\n")
            for expense in monthly_expenses:
                f.write(f"{expense.date}, {expense.name}, {expense.amount}, {expense.category}\n")
            total_expenditure = sum([ex.amount for ex in monthly_expenses])
            remaining_budget = budget - total_expenditure
            f.write(f"Total spent in {month}: ${total_expenditure:.2f}\n")
            f.write(f"Remaining budget for {month}: ${remaining_budget:.2f}\n\n")

    for month, monthly_expenses in expenses_by_month.items():
        amount_by_category = {}
        for expense in monthly_expenses:
            key = expense.category
            if key in amount_by_category:
                amount_by_category[key] += expense.amount
            else:
                amount_by_category[key] = expense.amount
        
        print(f"\nExpenditure for {month} 📈:")
        for key, amount in amount_by_category.items():
            print(f"  {key}: ${amount:.2f}")
        
        total_expenditure = sum([ex.amount for ex in monthly_expenses])
        print(f"Total spent in {month}: ${total_expenditure:.2f}")

        remaining_budget = budget - total_expenditure
        print(f"Remaining budget for {month}: ${remaining_budget:.2f}")

        now = datetime.datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        remaining_days = days_in_month - now.day

        daily_budget = remaining_budget / remaining_days
        print(f"Budget per Day for {month}: ${daily_budget:.2f}")

if __name__ == "__main__":
    main()