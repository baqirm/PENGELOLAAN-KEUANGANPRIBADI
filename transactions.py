import csv
import os
from datetime import datetime

TRANSACTION_FILE = "transactions.csv"

def initialize_transaction_file():
    if not os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "username", "type", "description", "amount", "date"])

initialize_transaction_file()

def read_transactions():
    with open(TRANSACTION_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        transactions = list(reader)
        for transaction in transactions:
            transaction["amount"] = float(transaction["amount"])
            transaction["date"] = datetime.strptime(transaction["date"], "%Y-%m-%d")
        return transactions

def write_transactions(transactions):
    with open(TRANSACTION_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "username", "type", "description", "amount", "date"])
        writer.writeheader()
        for transaction in transactions:
            transaction["date"] = transaction["date"].strftime("%Y-%m-%d")
            writer.writerow(transaction)

def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date > datetime.now():
            raise ValueError("Tanggal tidak boleh melebihi tanggal saat ini.")
        return date
    except ValueError as e:
        raise ValueError(f"Format tanggal salah atau {str(e)}")

def add_transaction(username, t_type, description, amount, date_str):
    transactions = read_transactions()
    date = validate_date(date_str)
    transactions.append({
        "id": len(transactions) + 1,
        "username": username,
        "type": t_type,
        "description": description,
        "amount": float(amount),
        "date": date
    })
    transactions.sort(key=lambda x: (x["date"].year, x["date"].month, x["date"].day))  
    write_transactions(transactions)
 

def get_user_transactions(username):
    transactions = read_transactions()  
    return [t for t in transactions if t["username"] == username]  

def get_monthly_summary(username, year, month):
    transactions = get_user_transactions(username)
    total_income = 0
    total_expense = 0

    for transaction in transactions:
        if transaction["date"].year == year and transaction["date"].month == month:
            if transaction["type"] == "Income":
                total_income += transaction["amount"]
            elif transaction["type"] == "Expense":
                total_expense += transaction["amount"]
    
    total_balance = total_income - total_expense
    return total_income, total_expense, total_balance

def get_yearly_summary(username, year):
    transactions = get_user_transactions(username)
    total_income = 0
    total_expense = 0

    for transaction in transactions:
        if transaction["date"].year == year:
            if transaction["type"] == "Income":
                total_income += transaction["amount"]
            elif transaction["type"] == "Expense":
                total_expense += transaction["amount"]
    
    total_balance = total_income - total_expense
    return total_income, total_expense, total_balance

def get_user_balance(username):
    transactions = get_user_transactions(username)
    total_income = 0
    total_expense = 0

    for transaction in transactions:
        amount = transaction["amount"]
        if transaction["type"] == "Income":
            total_income += amount
        elif transaction["type"] == "Expense":
            total_expense += amount
            
    total_balance = total_income - total_expense
    return total_income, total_expense, total_balance