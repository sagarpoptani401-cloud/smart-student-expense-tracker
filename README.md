# Smart Student Expense Tracker

A beginner-friendly Python project that helps college students manage a monthly budget and record everyday expenses.

## Problem statement
Students often spend money on food, travel, hostel needs, and study materials without tracking their total spending. This program provides a simple way to record expenses and compare them with a monthly budget.

## Objectives
- Set a monthly budget.
- Record expenses with date, category, amount, and description.
- View all recorded expenses.
- Calculate total spending, remaining budget, and budget usage.
- View spending totals by category.
- Save data between sessions.

## Features
- Menu-based command-line interface.
- Input validation for amounts and menu choices.
- Budget-overrun warning.
- Persistent storage in `expenses.json`.
- No third-party Python packages required.

## Technology used
- Python 3
- Python standard library: `json`, `pathlib`, and `datetime`

## How to run
1. Install Python 3 if it is not already installed.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python expense_tracker.py
   ```

   On some systems, use `python3 expense_tracker.py`.

5. Choose an option from the menu. Set your monthly budget first, then add expenses.

The file `expenses.json` is created automatically when you save your first budget or expense. Keep it in the same folder as the Python file.

## Example
```text
====== SMART STUDENT EXPENSE TRACKER ======
1. Set monthly budget
2. Add an expense
3. View all expenses
4. View spending summary
5. Exit
Choose an option (1-5): 1
Enter your monthly budget (₹): 5000
Monthly budget saved: ₹5000.00
```

## Python concepts demonstrated
- Variables and data types
- Functions
- `if-elif-else` conditions
- `while` and `for` loops
- Lists and dictionaries
- Exception handling with `try-except`
- Reading and writing JSON files
- Basic calculations

## Testing checklist
- [ ] Set a monthly budget.
- [ ] Add a food expense.
- [ ] Add a travel expense.
- [ ] View all expenses.
- [ ] Check the summary and category totals.
- [ ] Enter invalid text for an amount and confirm the program asks again.
- [ ] Restart the program and confirm saved data is still available.
- [ ] Add expenses above the budget and confirm the warning appears.

## Screenshots
Add your own screenshots here after running the program:
1. Main menu
2. Adding an expense
3. Expense list
4. Monthly summary

## Future improvements
- Add a graphical interface.
- Filter expenses by month.
- Export reports to CSV.
- Add an option to edit or delete an expense.

## Author
Student project for learning Python fundamentals. Add your name, course, and institution here before submission.
