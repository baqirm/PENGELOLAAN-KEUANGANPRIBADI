import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime 
from PIL import Image, ImageTk
import users as us 
import transactions as ts

root = tk.Tk()
root.title("Aplikasi Pengelolaan Uang")
root.geometry("1800x900")

theme_colors = {
    "button_bg": "white",
    "button_fg": "black"}

style = ttk.Style()
style.configure("TButton", background=theme_colors["button_bg"], foreground=theme_colors["button_fg"], font=("Adobe Garamond Pro Bold", 20))

def set_background_gif():
    global gif_frames, gif_index, gif_label, original_gif

    original_gif = Image.open("Adventure Time.gif")  
        
    gif_frames = []
    for frame in range(original_gif.n_frames):
        original_gif.seek(frame)
        resized_frame = original_gif.copy().resize((1600, 900), Image.LANCZOS)
        gif_frames.append(ImageTk.PhotoImage(resized_frame))

    gif_index = 0
    gif_label = tk.Label(root)
    gif_label.place(relwidth=1, relheight=1)
    update_gif()

def update_gif():
    global gif_index
    gif_label.config(image=gif_frames[gif_index])
    gif_index = (gif_index + 1) % len(gif_frames)
    root.after(200, update_gif)  

def clear_frame():
    for widget in root.winfo_children():
        if widget != gif_label:  
            widget.destroy()

    global back_icon
    back_icon = resize_image("BACK.png", (50, 50))

def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "Anda berhasil logout")
    show_home()

def sign_up_user():
    def submit_signup():
        username = entry_username.get()
        password = entry_password.get()
        email = entry_email.get()

        if username and password and email:
            result = us.sign_up(username, password, email)
            messagebox.showinfo("Sign Up", result)
            if result == "Registrasi berhasil!":
                show_home()
        else:
            messagebox.showerror("Error", "Harap isi semua kolom.")

    clear_frame()
    ttk.Label(root, text="Sign Up", font=("Adobe Garamond Pro Bold", 45), background="white").pack(pady=20)

    ttk.Label(root, text="Username:", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=10)
    entry_username = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_username.pack(pady=7)

    ttk.Label(root, text="Password:", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=10)
    entry_password = ttk.Entry(root, font=("Times New Roman", 18), width=23, show="*")
    entry_password.pack(pady=7)

    ttk.Label(root, text="Email:", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=10)
    entry_email = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_email.pack(pady=7)

    global sign_up_icon
    sign_up_icon = resize_image("SIGN UP.png", (50, 50))
    ttk.Button(root, text="Sign Up", image=sign_up_icon, compound=tk.LEFT, command=submit_signup).pack(pady=10)
    
    ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_home).pack(pady=10)

def sign_in_user():
    def submit_signin():
        username = entry_username.get()
        password = entry_password.get()
        user = us.sign_in(username, password)
        if isinstance(user, dict):
            global current_user
            current_user = user
            show_main_menu()
        else:
            messagebox.showerror("Error", user)
   
    clear_frame()
    ttk.Label(root, text="Sign In", font=("Adobe Garamond Pro Bold", 45), background="white").pack(pady=20)
    
    ttk.Label(root, text="Username:", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=10)
    entry_username = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_username.pack(pady=7)

    ttk.Label(root, text="Password:", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=10)
    entry_password = ttk.Entry(root, font=("Times New Roman", 18), width=23, show="*")
    entry_password.pack(pady=7)
    
    global sign_in_icon
    sign_in_icon = resize_image("SIGN IN.png", (50, 50))
    ttk.Button(root, text="Sign In", image=sign_in_icon, compound=tk.LEFT, command=submit_signin).pack(pady=10)
    
    ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_home).pack(pady=10)

def add_transaction_user():
    def save_transaction():
        t_type = transaction_type.get()
        description = entry_description.get()
        amount = entry_amount.get()
        date = entry_date.get()

        if not amount.replace('.', '',).replace(',', '', 1).isdigit():  
            messagebox.showerror("Error", "Jumlah harus berupa angka.")
            return

        try:
            validated_date = ts.validate_date(date) 
            amount = amount.replace('.', '').replace(',', '')
            ts.add_transaction(current_user["username"], t_type, description, amount, validated_date.strftime("%Y-%m-%d"))
            messagebox.showinfo("Success", "Transaksi berhasil disimpan.")
            show_main_menu()
        except ValueError as e:
            messagebox.showerror("Error", str(e)) 

    clear_frame()
    ttk.Label(root, text="Tambah Transaksi", font=("Adobe Garamond Pro Bold", 45), background="white").pack(pady=20)

    ttk.Label(root, text="Tipe Transaksi: ", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=8)
    transaction_type = ttk.Combobox(root, font=("Times New Roman", 18), width=23, values=["Income", "Expense"])
    transaction_type.pack(pady=5)

    ttk.Label(root, text="Deskripsi:", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=8)
    entry_description = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_description.pack(pady=5)

    ttk.Label(root, text="Jumlah:", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=8)
    entry_amount = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_amount.pack(pady=5)

    ttk.Label(root, text="Tanggal (YYYY-MM-DD):", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=8)
    entry_date = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_date.pack(pady=5)
    
    global save_icon
    save_icon = resize_image("SAVE NEW.png", (50, 50))
    ttk.Button(root, text="Simpan", image=save_icon, compound=tk.LEFT, command=save_transaction).pack(pady=10)
    
    ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_main_menu).pack(pady=10)

def show_report():
    def show_monthly_report():
        def generate_monthly_report():
            selected_month = month_combobox.get()
            selected_year = int(year_combobox.get())
            month_map = {"Januari": 1, "Februari": 2, "Maret": 3, "April": 4, "Mei": 5, "Juni": 6, "Juli": 7, "Agustus": 8, "September": 9, "Oktober": 10, "November": 11, "Desember": 12}
            
            month = month_map[selected_month]
            income, expense, balance = ts.get_monthly_summary(current_user["username"], selected_year, month)
            transactions = ts.get_user_transactions(current_user["username"])
            monthly_transactions = [t for t in transactions if t["date"].year == selected_year and t["date"].month == month]
            
            clear_frame()
            ttk.Label(root, text=f"Laporan Bulanan - {selected_month} {selected_year}", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=20)
            
            frame = ttk.Frame(root)
            frame.pack()
            
            columns = ("type", "description", "amount", "date")
            tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

            tree.heading("type", text="Tipe Transaksi")
            tree.heading("description", text="Deskripsi")
            tree.heading("amount", text="Jumlah")
            tree.heading("date", text="Tanggal")

            tree.column("type", anchor="center", width=150)
            tree.column("description", anchor="center", width=300)
            tree.column("amount", anchor="center", width=150)
            tree.column("date", anchor="center", width=150)

            tree.pack(fill="both", expand=True, pady=10)

            for transaction in monthly_transactions:
                formatted_amount = f"{transaction['amount']:,.0f}".replace(",", ".")
                tree.insert("", "end", values=(transaction["type"], transaction["description"], formatted_amount, transaction["date"].strftime("%Y-%m-%d")))

            formatted_income = f"{income:,.0f}".replace(",", ".")
            formatted_expense = f"{expense:,.0f}".replace(",", ".")
            formatted_balance = f"{balance:,.0f}".replace(",", ".")

            ttk.Label(frame, text=f"Total Pendapatan: {formatted_income}", font=("Adobe Garamond Pro Bold", 16, "bold"), foreground="green").pack(pady=5)
            ttk.Label(frame, text=f"Total Pengeluaran: {formatted_expense}", font=("Adobe Garamond Pro Bold", 16, "bold"), foreground="red").pack(pady=5)
            ttk.Label(frame, text=f"Saldo Bulanan: {formatted_balance}", font=("Adobe Garamond Pro Bold", 16, "bold"), foreground="blue").pack(pady=5)
            
            ttk.Button(root, text="Kembali",  image=back_icon, compound=tk.LEFT, command=show_report).pack(pady=10)

        clear_frame()
        ttk.Label(root, text="Pilih Bulan dan Tahun", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=20)

        month_combobox = ttk.Combobox(root, values=["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"], font=("Adobe Garamond Pro Bold", 18))
        month_combobox.pack(pady=10)
        
        year_combobox = ttk.Combobox(root, values=list(range(2000, datetime.now().year + 1)), font=("Times New Roman", 18))
        year_combobox.pack(pady=10)

        ttk.Button(root, text="Tampilkan", image=monthandyear_icon, compound=tk.LEFT, command=generate_monthly_report).pack(pady=10)
        ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_report).pack(pady=10)

    def show_yearly_report():
        def generate_yearly_report():
            selected_year = int(year_combobox.get())
            income, expense, balance = ts.get_yearly_summary(current_user["username"], selected_year)
            transactions = ts.get_user_transactions(current_user["username"])
            
            monthly_summary = {}
            for transaction in transactions:
                if transaction["date"].year == selected_year:
                    month = transaction["date"].month
                    if month not in monthly_summary:
                        monthly_summary[month] = {"income": 0, "expense": 0}
                    if transaction["type"] == "Income":
                        monthly_summary[month]["income"] += transaction["amount"]
                    elif transaction["type"] == "Expense":
                        monthly_summary[month]["expense"] += transaction["amount"]

            total_income = sum(summary["income"] for summary in monthly_summary.values())
            total_expense = sum(summary["expense"] for summary in monthly_summary.values())
            total_balance = total_income - total_expense

            clear_frame()
            ttk.Label(root, text=f"Laporan Tahunan - {selected_year}", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=20)
            
            frame = ttk.Frame(root)
            frame.pack()

            columns = ("month", "income", "expense", "balance")
            tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
            tree.heading("month", text="Bulan")
            tree.heading("income", text="Pendapatan")
            tree.heading("expense", text="Pengeluaran")
            tree.heading("balance", text="Saldo")

            tree.column("month", anchor="center", width=150)
            tree.column("income", anchor="center", width=150)
            tree.column("expense", anchor="center", width=150)
            tree.column("balance", anchor="center", width=150)

            tree.pack(fill="both", expand=True, pady=10)

            month_names = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

            for month, summary in sorted(monthly_summary.items()):
                income = summary["income"]
                expense = summary["expense"]
                balance = income - expense
                formatted_income = f"{income:,.0f}".replace(",", ".")
                formatted_expense = f"{expense:,.0f}".replace(",", ".")
                formatted_balance = f"{balance:,.0f}".replace(",", ".")
                tree.insert("", "end", values=(month_names[month - 1], formatted_income, formatted_expense, formatted_balance))

            formatted_total_income = f"{total_income:,.0f}".replace(",", ".")
            formatted_total_expense = f"{total_expense:,.0f}".replace(",", ".")
            formatted_total_balance = f"{total_balance:,.0f}".replace(",", ".")

            ttk.Label(frame, text=f"Total Pendapatan Tahunan: {formatted_total_income}", font=("Adobe Garamond Pro Bold", 16, "bold"), foreground="green").pack(pady=5)
            ttk.Label(frame, text=f"Total Pengeluaran Tahunan: {formatted_total_expense}", font=("Adobe Garamond Pro Bold", 16, "bold"), foreground="red").pack(pady=5)
            ttk.Label(frame, text=f"Saldo Akhir Tahunan: {formatted_total_balance}", font=("Adobe Garamond Pro Bold", 16, "bold"), foreground="blue").pack(pady=5)
            
            ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_report).pack(pady=10)
        clear_frame()
        ttk.Label(root, text="Pilih Tahun", font=("Adobe Garamond Pro Bold", 30), background="white").pack(pady=20)

        year_combobox = ttk.Combobox(root, values=list(range(2000, datetime.now().year + 1)), font=("Adobe Garamond Pro Bold", 18))
        year_combobox.pack(pady=10)

        ttk.Button(root, text="Tampilkan", image=monthandyear_icon, compound=tk.LEFT, command=generate_yearly_report).pack(pady=10)
        ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_report).pack(pady=10)

    clear_frame()

    ttk.Label(root, text="Laporan Keuangan", font=("Adobe Garamond Pro Bold", 45), background="white").pack(pady=20)
    
    global monthandyear_icon
    monthandyear_icon = resize_image("LAPORAN KEUANGAN ICON.png", (50,50))
    ttk.Button(root, text="Laporan Per Bulan", image=monthandyear_icon, compound=tk.LEFT, command=show_monthly_report).pack(pady=10)
    ttk.Button(root, text="Laporan Per Tahun", image=monthandyear_icon, compound=tk.LEFT, command=show_yearly_report).pack(pady=10)
    ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_main_menu).pack(pady=10)
    
    style = ttk.Style()
    style.configure("Treeview", font=("Adobe Garamond Pro Bold", 12))
    style.configure("Treeview.Heading", font=("Adobe Garamond Pro Bold", 14), foreground="blue")
    
def show_main_menu():
    clear_frame()

    ttk.Label(root, text=f"Selamat Datang, {current_user['username']}", font=("Adobe Garamond Pro Bold", 45), background="white").pack(pady=20)
    
    global transaksi_icon, laporan_icon, logout_icon
    transaksi_icon = resize_image("TRANSACTION NEW.png", (50,50))
    laporan_icon = resize_image("LAPORAN KEUANGAN.png", (50,50))
    logout_icon = resize_image("LOGOUT.png", (50,50))
    
    ttk.Button(root, text="Tambah Transaksi", image=transaksi_icon, compound=tk.LEFT, command=add_transaction_user).place(relx=0.5, rely=0.2, anchor="center")
    ttk.Button(root, text="Lihat Laporan", image=laporan_icon, compound=tk.LEFT, command=show_report).place(relx=0.5, rely=0.3, anchor="center")
    ttk.Button(root, text="Logout", image=logout_icon, compound=tk.LEFT, command=logout).place(relx=0.5, rely=0.4, anchor="center")
    
def resize_image(image_path, size):
    image = Image.open(image_path)
    resized_image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

def show_home():
    clear_frame()

    label = ttk.Label(root, text="Aplikasi Pengelolaan Uang", font=("Adobe Garamond Pro Bold", 45), background='white', foreground='Black')
    label.pack(pady=20)

    global sign_in, sign_up
    sign_up = resize_image("SIGN UP.png", (70, 70))  
    sign_in = resize_image("SIGN IN.png", (70, 70))  

    ttk.Button(root, text="Sign Up", image=sign_up, compound=tk.LEFT, command=sign_up_user).place(relx=0.5, rely=0.4, anchor="center")
    ttk.Button(root, text="Sign In", image=sign_in, compound=tk.LEFT, command=sign_in_user).place(relx=0.5, rely=0.5, anchor="center")
    
set_background_gif()

current_user = None

show_home()

root.mainloop()