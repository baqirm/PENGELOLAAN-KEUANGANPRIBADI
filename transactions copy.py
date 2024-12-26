import csv
import os

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
        return transactions

def write_transactions(transactions):
    with open(TRANSACTION_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "username", "type", "description", "amount", "date"])
        writer.writeheader()  
        writer.writerows(transactions)  

def add_transaction(username, t_type, description, amount, date):
    transactions = read_transactions() 
    transaction_id = len(transactions) + 1  
    try:
        amount = float(amount)  
    except ValueError:
        raise ValueError("Jumlah harus berupa angka.")
    
    transactions.append({
        "id": transaction_id,
        "username": username,
        "type": t_type,
        "description": description,
        "amount": amount,
        "date": date
    })
    write_transactions(transactions)  

def get_user_transactions(username):
    transactions = read_transactions()  
    return [t for t in transactions if t["username"] == username]  

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