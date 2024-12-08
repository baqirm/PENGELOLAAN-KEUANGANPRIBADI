import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

# File CSV untuk penyimpanan data
USER_FILE = "users.csv"
TRANSACTION_FILE = "transactions.csv"

# Inisialisasi file CSV jika belum ada
def initialize_files():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "username", "password"])  # Header

# Inisialisasi file transaksi jika belum ada
def initialize_transaction_file():
    if not os.path.exists(TRANSACTION_FILE):
        with open(TRANSACTION_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "user_id", "type", "amount", "date"])  # Header
        print(f"File '{TRANSACTION_FILE}' berhasil dibuat.")
    else:
        print(f"File '{TRANSACTION_FILE}' sudah ada.")

# Panggil fungsi untuk membuat file transaksi
initialize_transaction_file()

# Fungsi untuk membaca CSV
def read_csv(file_path):
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)

# Fungsi untuk menulis ke CSV
def write_csv(file_path, data, headers):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

# Fungsi Sign Up
def sign_up():
    def submit_signup():
        username = entry_username.get()
        password = entry_password.get()

        if username and password:
            users = read_csv(USER_FILE)
            if any(user["username"] == username for user in users):
                messagebox.showerror("Error", "Username sudah terdaftar.")
            else:
                user_id = len(users) + 1
                users.append({"id": user_id, "username": username, "password": password})
                write_csv(USER_FILE, users, ["id", "username", "password"])
                messagebox.showinfo("Success", "Sign Up berhasil!")
                signup_window.destroy()
        else:
            messagebox.showerror("Error", "Harap isi semua kolom.")

    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")

    tk.Label(signup_window, text="Username:").pack(pady=5)
    entry_username = tk.Entry(signup_window)
    entry_username.pack(pady=5)

    tk.Label(signup_window, text="Password:").pack(pady=5)
    entry_password = tk.Entry(signup_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(signup_window, text="Sign Up", command=submit_signup).pack(pady=10)

# Fungsi Sign In
def sign_in():
    def submit_signin():
        username = entry_username.get()
        password = entry_password.get()

        users = read_csv(USER_FILE)
        user = next((u for u in users if u["username"] == username and u["password"] == password), None)

        if user:
            messagebox.showinfo("Success", f"Selamat datang, {username}!")
            global current_user
            current_user = user
            signin_window.destroy()
            main_menu()
        else:
            messagebox.showerror("Error", "Username atau password salah.")

    signin_window = tk.Toplevel(root)
    signin_window.title("Sign In")

    tk.Label(signin_window, text="Username:").pack(pady=5)
    entry_username = tk.Entry(signin_window)
    entry_username.pack(pady=5)

    tk.Label(signin_window, text="Password:").pack(pady=5)
    entry_password = tk.Entry(signin_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(signin_window, text="Sign In", command=submit_signin).pack(pady=10)

# Menu Utama
def main_menu():
    def add_transaction():
        def save_transaction():
            t_type = transaction_type.get()
            amount = entry_amount.get()
            date = entry_date.get()

            if t_type and amount and date:
                try:
                    transactions = read_csv(TRANSACTION_FILE)
                    transaction_id = len(transactions) + 1
                    transactions.append({
                        "id": transaction_id,
                        "user_id": current_user["id"],
                        "type": t_type,
                        "amount": amount,
                        "date": date
                    })
                    write_csv(TRANSACTION_FILE, transactions, ["id", "user_id", "type", "amount", "date"])
                    messagebox.showinfo("Success", "Transaksi berhasil disimpan.")
                    transaction_window.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Jumlah harus berupa angka.")
            else:
                messagebox.showerror("Error", "Harap isi semua kolom.")

        transaction_window = tk.Toplevel(root)
        transaction_window.title("Tambah Transaksi")

        tk.Label(transaction_window, text="Tipe Transaksi:").pack(pady=5)
        transaction_type = ttk.Combobox(transaction_window, values=["income", "expense"])
        transaction_type.pack(pady=5)

        tk.Label(transaction_window, text="Jumlah:").pack(pady=5)
        entry_amount = tk.Entry(transaction_window)
        entry_amount.pack(pady=5)

        tk.Label(transaction_window, text="Tanggal (YYYY-MM-DD):").pack(pady=5)
        entry_date = tk.Entry(transaction_window)
        entry_date.pack(pady=5)

        tk.Button(transaction_window, text="Simpan", command=save_transaction).pack(pady=10)

    def view_report():
        def generate_report():
            start_date = entry_start_date.get()
            end_date = entry_end_date.get()

            transactions = read_csv(TRANSACTION_FILE)
            user_transactions = [t for t in transactions if t["user_id"] == current_user["id"] and start_date <= t["date"] <= end_date]

            report_text.delete(1.0, tk.END)
            total_income = 0
            total_expense = 0

            for t in user_transactions:
                t_type, amount, date = t["type"], float(t["amount"]), t["date"]
                if t_type == "income":
                    total_income += amount
                else:
                    total_expense += amount
                report_text.insert(tk.END, f"{date} - {t_type} - {amount}\\n")

            total_balance = total_income - total_expense
            report_text.insert(tk.END, f"\\nTotal Income: {total_income}\\n")
            report_text.insert(tk.END, f"Total Expense: {total_expense}\\n")
            report_text.insert(tk.END, f"Total Balance: {total_balance}\\n")

        report_window = tk.Toplevel(root)
        report_window.title("Laporan Keuangan")

        tk.Label(report_window, text="Tanggal Mulai (YYYY-MM-DD):").pack(pady=5)
        entry_start_date = tk.Entry(report_window)
        entry_start_date.pack(pady=5)

        tk.Label(report_window, text="Tanggal Akhir (YYYY-MM-DD):").pack(pady=5)
        entry_end_date = tk.Entry(report_window)
        entry_end_date.pack(pady=5)

        tk.Button(report_window, text="Tampilkan Laporan", command=generate_report).pack(pady=10)

        report_text = tk.Text(report_window, width=50, height=20)
        report_text.pack(pady=5)

    main_menu_window = tk.Toplevel(root)
    main_menu_window.title("Menu Utama")

    tk.Button(main_menu_window, text="Tambah Transaksi", command=add_transaction).pack(pady=10)
    tk.Button(main_menu_window, text="Lihat Laporan", command=view_report).pack(pady=10)

# Main Application
initialize_files()

root = tk.Tk()
root.title("Aplikasi Pengelolaan Uang Pribadi")

current_user = None

welcome_label = tk.Label(root, text="Selamat Datang di Aplikasi Pengelolaan Uang", font=("Arial", 16))
welcome_label.pack(pady=20)

tk.Button(root, text="Sign Up", command=sign_up).pack(pady=10)
tk.Button(root, text="Sign In", command=sign_in).pack(pady=10)

root.mainloop()
