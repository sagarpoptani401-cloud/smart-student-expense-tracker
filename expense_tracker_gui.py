import json
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import date

DATA_FILE = Path(__file__).with_name("expenses.json")

def load_data():
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "budget" in data and "expenses" in data:
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return {"budget": 0.0, "expenses": []}

data = load_data()

def save_data():
    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except OSError as error:
        messagebox.showerror("Save error", f"Could not save data:\n{error}")

def money(amount):
    return f"₹{amount:,.2f}"

def total_spending():
    return sum(float(item.get("amount", 0)) for item in data["expenses"])

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    for item in reversed(data["expenses"]):
        tree.insert("", "end", values=(item.get("date", ""), item.get("category", "Other"), money(float(item.get("amount", 0))), item.get("description", "")))

def refresh_summary():
    total = total_spending()
    budget = float(data.get("budget", 0))
    remaining = budget - total
    budget_value.config(text=money(budget))
    spent_value.config(text=money(total))
    remaining_value.config(text=money(remaining), foreground="#b91c1c" if remaining < 0 else "#166534")
    usage_value.config(text=f"{(total / budget) * 100:.1f}% of budget used" if budget > 0 else "Set a budget to track progress")
    status_value.config(text=(f"Over budget by {money(total - budget)}" if budget > 0 and total > budget else "You're within your budget." if budget > 0 else "Set a monthly budget to get started."))
    refresh_table()

def set_budget():
    try:
        amount = float(budget_entry.get().strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid budget", "Enter a number greater than zero, e.g. 5000.")
        return
    data["budget"] = round(amount, 2)
    save_data()
    budget_entry.delete(0, tk.END)
    refresh_summary()
    messagebox.showinfo("Budget saved", f"Monthly budget saved: {money(amount)}")

def add_expense():
    try:
        amount = float(amount_entry.get().strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid amount", "Enter an amount greater than zero, e.g. 150.")
        return
    category = category_box.get().strip()
    if not category:
        messagebox.showerror("Missing category", "Please select a category.")
        return
    description = description_entry.get().strip() or "No description"
    data["expenses"].append({"date": date.today().isoformat(), "amount": round(amount, 2), "category": category, "description": description})
    save_data()
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_box.set("Food")
    refresh_summary()
    messagebox.showinfo("Expense added", f"Recorded {money(amount)} for {category}.")
    amount_entry.focus_set()

def clear_expenses():
    if not data["expenses"]:
        messagebox.showinfo("No expenses", "There are no expenses to clear.")
        return
    if messagebox.askyesno("Clear all expenses", "Permanently remove all recorded expenses?"):
        data["expenses"] = []
        save_data()
        refresh_summary()

root = tk.Tk()
root.title("Smart Student Expense Tracker")
root.geometry("1000x700")
root.minsize(820, 600)
root.configure(bg="#f3f6fb")
style = ttk.Style(root)
try:
    style.theme_use("clam")
except tk.TclError:
    pass
style.configure("TFrame", background="#f3f6fb")
style.configure("Card.TFrame", background="#ffffff")
style.configure("TLabel", background="#f3f6fb", foreground="#172033", font=("Segoe UI", 10))
style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"), foreground="#13264a")
style.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground="#61708a")
style.configure("CardTitle.TLabel", background="#ffffff", font=("Segoe UI", 10, "bold"), foreground="#61708a")
style.configure("Metric.TLabel", background="#ffffff", font=("Segoe UI", 19, "bold"), foreground="#13264a")
style.configure("TButton", font=("Segoe UI", 10), padding=(10, 7))
style.configure("Accent.TButton", background="#2457d6", foreground="#ffffff")
style.map("Accent.TButton", background=[("active", "#1d46ae")])

main = ttk.Frame(root, padding=22)
main.pack(fill="both", expand=True)
ttk.Label(main, text="Smart Student Expense Tracker", style="Title.TLabel").pack(anchor="w")
ttk.Label(main, text="Manage your student budget, one expense at a time.", style="Subtitle.TLabel").pack(anchor="w", pady=(4, 18))
metrics = ttk.Frame(main)
metrics.pack(fill="x", pady=(0, 12))
for c in range(3): metrics.columnconfigure(c, weight=1)
def metric_card(column, title):
    card = ttk.Frame(metrics, style="Card.TFrame", padding=14)
    card.grid(row=0, column=column, sticky="nsew", padx=5)
    ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
    value = ttk.Label(card, text="₹0.00", style="Metric.TLabel")
    value.pack(anchor="w", pady=(7, 0))
    return value
budget_value = metric_card(0, "MONTHLY BUDGET")
spent_value = metric_card(1, "TOTAL SPENT")
remaining_value = metric_card(2, "REMAINING BUDGET")
status_row = ttk.Frame(main)
status_row.pack(fill="x", pady=(0, 14))
usage_value = ttk.Label(status_row, text="")
usage_value.pack(side="left")
status_value = ttk.Label(status_row, text="")
status_value.pack(side="right")
forms = ttk.Frame(main)
forms.pack(fill="x", pady=(0, 14))
forms.columnconfigure(0, weight=1)
forms.columnconfigure(1, weight=2)
budget_card = ttk.Frame(forms, style="Card.TFrame", padding=13)
budget_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
ttk.Label(budget_card, text="Set monthly budget", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 8))
budget_row = ttk.Frame(budget_card, style="Card.TFrame")
budget_row.pack(fill="x")
budget_entry = ttk.Entry(budget_row)
budget_entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0, 7))
if data.get("budget", 0): budget_entry.insert(0, str(data["budget"]))
ttk.Button(budget_row, text="Save budget", style="Accent.TButton", command=set_budget).pack(side="left")
expense_card = ttk.Frame(forms, style="Card.TFrame", padding=13)
expense_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
ttk.Label(expense_card, text="Add an expense", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))
for col, label in enumerate(("Amount (₹)", "Category", "Description", "")):
    ttk.Label(expense_card, text=label).grid(row=1, column=col, sticky="w", padx=4)
amount_entry = ttk.Entry(expense_card, width=11)
amount_entry.grid(row=2, column=0, sticky="ew", padx=4, ipady=4)
category_box = ttk.Combobox(expense_card, values=["Food", "Travel", "Hostel", "Study", "Shopping", "Other"], state="readonly", width=11)
category_box.set("Food")
category_box.grid(row=2, column=1, sticky="ew", padx=4, ipady=3)
description_entry = ttk.Entry(expense_card, width=16)
description_entry.grid(row=2, column=2, sticky="ew", padx=4, ipady=4)
ttk.Button(expense_card, text="Add", style="Accent.TButton", command=add_expense).grid(row=2, column=3, padx=4)
for col in range(4): expense_card.columnconfigure(col, weight=1)
table_card = ttk.Frame(main, style="Card.TFrame", padding=13)
table_card.pack(fill="both", expand=True)
table_header = ttk.Frame(table_card, style="Card.TFrame")
table_header.pack(fill="x", pady=(0, 8))
ttk.Label(table_header, text="Recent expenses", style="CardTitle.TLabel").pack(side="left")
ttk.Button(table_header, text="Clear all expenses", command=clear_expenses).pack(side="right")
tree = ttk.Treeview(table_card, columns=("date", "category", "amount", "description"), show="headings")
for col, title in (("date", "Date"), ("category", "Category"), ("amount", "Amount"), ("description", "Description")):
    tree.heading(col, text=title)
tree.column("date", width=120, anchor="center")
tree.column("category", width=130, anchor="center")
tree.column("amount", width=130, anchor="e")
tree.column("description", width=400)
scroll = ttk.Scrollbar(table_card, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")
ttk.Label(main, text="Your data is saved locally in expenses.json.", style="Subtitle.TLabel").pack(anchor="w", pady=(8, 0))
refresh_summary()
root.mainloop()
