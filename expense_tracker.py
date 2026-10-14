import json
from pathlib import Path
from datetime import date

DATA_FILE = Path("expenses.json")


def load_data():
    """Load saved data, or return a blank budget and expense list."""
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict) and "budget" in data and "expenses" in data:
                return data
        except (json.JSONDecodeError, OSError):
            print("Warning: saved data could not be read. Starting with empty data.")
    return {"budget": 0.0, "expenses": []}


def save_data(data):
    """Save the budget and expenses to a JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def read_amount(prompt):
    """Read a positive amount from the user."""
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount <= 0:
                print("Please enter an amount greater than zero.")
            else:
                return round(amount, 2)
        except ValueError:
            print("Invalid amount. Please enter a number, such as 120 or 99.50.")


def set_budget(data):
    data["budget"] = read_amount("Enter your monthly budget (₹): ")
    save_data(data)
    print(f"Monthly budget saved: ₹{data['budget']:.2f}")


def add_expense(data):
    amount = read_amount("Expense amount (₹): ")
    category = input("Category (Food/Travel/Hostel/Study/Other): ").strip()
    description = input("Short description: ").strip()

    if not category:
        category = "Other"
    if not description:
        description = "No description"

    expense = {
        "date": date.today().isoformat(),
        "amount": amount,
        "category": category,
        "description": description,
    }
    data["expenses"].append(expense)
    save_data(data)
    print("Expense added successfully!")

    total = sum(item["amount"] for item in data["expenses"])
    if data["budget"] > 0 and total > data["budget"]:
        print("Warning: Your total expenses have exceeded your monthly budget.")


def view_expenses(data):
    if not data["expenses"]:
        print("No expenses recorded yet.")
        return

    print("\n" + "-" * 76)
    print(f"{'No.':<5}{'Date':<13}{'Category':<16}{'Amount (₹)':>13}  Description")
    print("-" * 76)
    for index, item in enumerate(data["expenses"], start=1):
        print(
            f"{index:<5}{item.get('date', ''):<13}"
            f"{item.get('category', 'Other')[:15]:<16}"
            f"{item.get('amount', 0):>13.2f}  "
            f"{item.get('description', '')}"
        )
    print("-" * 76)


def show_summary(data):
    total = sum(item["amount"] for item in data["expenses"])
    budget = data["budget"]
    remaining = budget - total

    print("\n========== MONTHLY SUMMARY ==========")
    print(f"Monthly budget : ₹{budget:.2f}")
    print(f"Total expenses : ₹{total:.2f}")
    if budget > 0:
        print(f"Remaining      : ₹{remaining:.2f}")
        if remaining < 0:
            print(f"Over budget by : ₹{abs(remaining):.2f}")
        else:
            print(f"Budget used    : {(total / budget) * 100:.1f}%")
    else:
        print("Remaining      : Set a budget to calculate this.")
    print("=====================================")

    if data["expenses"]:
        totals_by_category = {}
        for item in data["expenses"]:
            category = item.get("category", "Other")
            totals_by_category[category] = totals_by_category.get(category, 0) + item["amount"]
        print("\nSpending by category:")
        for category, amount in sorted(totals_by_category.items()):
            print(f"  {category}: ₹{amount:.2f}")


def main():
    data = load_data()
    while True:
        print("\n====== SMART STUDENT EXPENSE TRACKER ======")
        print("1. Set monthly budget")
        print("2. Add an expense")
        print("3. View all expenses")
        print("4. View spending summary")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            set_budget(data)
        elif choice == "2":
            add_expense(data)
        elif choice == "3":
            view_expenses(data)
        elif choice == "4":
            show_summary(data)
        elif choice == "5":
            print("Your data is saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
