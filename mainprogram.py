import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from PIL import Image, ImageTk
import user as us 
import transactions as ts

# Inisialisasi aplikasi
root = tk.Tk()
root.title("Aplikasi Pengelolaan Uang")
root.geometry("1600x900")

# Mengatur tema warna
theme_colors = {
    "button_bg": "white",
    "button_fg": "black"}

# Mengonfigurasi gaya tombol
style = ttk.Style()
style.configure("TButton", background=theme_colors["button_bg"], foreground=theme_colors["button_fg"], font=("Adventure Time Logo", 20))

# Fungsi untuk memuat dan menampilkan GIF sebagai latar belakang
def set_background_gif():
    global gif_frames, gif_index, gif_label, original_gif
    try:
        original_gif = Image.open("Adventure Time.gif")  
        print("GIF loaded successfully!")
    except Exception as e:
        print(f"Error loading GIF: {e}")
        return

    gif_frames = []
    for frame in range(original_gif.n_frames):
        original_gif.seek(frame)
        resized_frame = original_gif.copy().resize((1600, 900), Image.LANCZOS)
        gif_frames.append(ImageTk.PhotoImage(resized_frame))

    gif_index = 0
    gif_label = tk.Label(root)
    gif_label.place(relwidth=1, relheight=1)
    update_gif()

# Fungsi untuk memperbarui frame GIF
def update_gif():
    global gif_index
    gif_label.config(image=gif_frames[gif_index])
    gif_index = (gif_index + 1) % len(gif_frames)
    root.after(200, update_gif)  

# Fungsi untuk membersihkan frame utama
def clear_frame():
    for widget in root.winfo_children():
        if widget != gif_label:  
            widget.destroy()

# Fungsi logout
def logout():
    global current_user
    current_user = None
    messagebox.showinfo("Logout", "Anda berhasil logout")
    show_home()

# Fungsi untuk sign up
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
    ttk.Label(root, text="Sign Up", font=("Adventure Time Logo", 45), background="white").pack(pady=20)

    ttk.Label(root, text="Username:", font=("Adventure Time Logo", 30), background="white").pack(pady=10)
    entry_username = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_username.pack(pady=7)

    ttk.Label(root, text="Password:", font=("Adventure Time Logo", 30), background="white").pack(pady=10)
    entry_password = ttk.Entry(root, font=("Times New Roman", 18), width=23, show="*")
    entry_password.pack(pady=7)

    ttk.Label(root, text="Email:", font=("Adventure Time Logo", 30), background="white").pack(pady=10)
    entry_email = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_email.pack(pady=7)

    global sign_up_icon
    sign_up_icon = resize_image("SIGN UP.png", (50, 50))
    ttk.Button(root, text="Sign Up", image=sign_up_icon, compound=tk.LEFT, command=submit_signup).pack(pady=10)
    
    global back_icon
    back_icon = resize_image("BACK.png", (50, 50))
    ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_home).pack(pady=10)

# Fungsi untuk sign in
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
    ttk.Label(root, text="Sign In", font=("Adventure Time Logo", 45), background="white").pack(pady=20)
    
    ttk.Label(root, text="Username:", font=("Adventure Time Logo", 30), background="white").pack(pady=10)
    entry_username = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_username.pack(pady=7)

    ttk.Label(root, text="Password:", font=("Adventure Time Logo", 30), background="white").pack(pady=10)
    entry_password = ttk.Entry(root, font=("Times New Roman", 18), width=23, show="*")
    entry_password.pack(pady=7)
    
    global sign_in_icon
    sign_in_icon = resize_image("SIGN IN.png", (50, 50))
    ttk.Button(root, text="Sign In", image=sign_in_icon, compound=tk.LEFT, command=submit_signin).pack(pady=10)
    
    global back_icon
    back_icon = resize_image("BACK.png", (50, 50))
    ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_home).pack(pady=10)

# transaction
def add_transaction_user():
    def save_transaction():
        t_type = transaction_type.get()
        description = entry_description.get()
        amount = entry_amount.get()
        date = entry_date.get()

        if t_type and description and amount and date:
            try:
                amount = (amount.replace('.', '').replace(',', ''))
                ts.add_transaction(current_user["username"], t_type, description, amount, date)
                messagebox.showinfo("Success", "Transaksi berhasil disimpan.")
                show_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Jumlah harus berupa angka.")
        else:
            messagebox.showerror("Error", "Harap isi semua kolom.")
            

    clear_frame()
    ttk.Label(root, text="Tambah Transaksi", font=("Adventure Time Logo", 45), background="white").pack(pady=20)

    ttk.Label(root, text="Tipe Transaksi: ", font=("Adventure Time Logo", 30), background="white").pack(pady=10)
    transaction_type = ttk.Combobox(root, font=("Times New Roman", 18), width=23, values=["Income", "Expense"])
    transaction_type.pack(pady=7)

    ttk.Label(root, text="Deskripsi:", font=("Adventure Time Logo", 30), background="white").pack(pady=10)
    entry_description = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_description.pack(pady=7)

    ttk.Label(root, text="Jumlah:", font=("Adventure Time Logo", 30), background="white").pack(pady=10)
    entry_amount = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_amount.pack(pady=7)

    ttk.Label(root, text="Tanggal (YYYY-MM-DD):", font=("Adventure Time Logo", 30), background="white").pack(pady=10)
    entry_date = ttk.Entry(root, font=("Times New Roman", 18), width=23)
    entry_date.pack(pady=7)
    
    global save_icon
    save_icon = resize_image("SAVE NEW.png", (50, 50))
    ttk.Button(root, text="Simpan", image=save_icon, compound=tk.LEFT, command=save_transaction).pack(pady=10)
    
    ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_main_menu).pack(pady=10)

# Fungsi untuk menampilkan laporan keuangan dalam bentuk tabel
def show_report():
    clear_frame()
    
    ttk.Label(root, text="Laporan Keuangan", font=("Adventure Time Logo", 45), background="white").pack(pady=20)

    frame = ttk.Frame(root, width=800, height=400)
    frame.pack()

    # Membuat style untuk Treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Times New Roman", 14,))
    style.configure("Treeview.Heading", font=("Times New Roman", 16,), foreground="blue")

    columns = ("type", "description", "amount", "date")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
    tree.heading("type", text="Tipe Transaksi")
    tree.heading("description", text="Deskripsi")
    tree.heading("amount", text="Jumlah")
    tree.heading("date", text="Tanggal")
    
    tree.column("type", anchor="center", width=165)
    tree.column("description", anchor="center", width=285)
    tree.column("amount", anchor="center", width=165)
    tree.column("date", anchor="center", width=165)
    
    tree.pack(fill="both", expand=True, pady=10)

    transactions = ts.get_user_transactions(current_user["username"])
    for transaction in transactions:
        formatted_amount = f"{float(transaction['amount']):,.0f}".replace(',', '.')
        tree.insert("", "end", values=(transaction["type"], transaction["description"], formatted_amount, transaction["date"]))

    # Menghitung dan menampilkan saldo
    total_income, total_expense, total_balance = ts.get_user_balance(current_user["username"])
    print(f"Total Income: {total_income}, Total Expense: {total_expense}, Total Balance: {total_balance}")  

    formatted_income = f"{total_income:,.0f}".replace(',', '.')
    formatted_expense = f"{total_expense:,.0f}".replace(',', '.')
    formatted_balance = f"{total_balance:,.0f}".replace(',', '.')

    # Menampilkan saldo
    ttk.Label(frame, text=f"Total Pendapatan: {formatted_income}", font=("Times New Roman", 16, "bold"), foreground="purple").pack(pady=10)
    ttk.Label(frame, text=f"Total Pengeluaran: {formatted_expense}", font=("Times New Roman", 16, "bold"), foreground="red").pack(pady=10)
    ttk.Label(frame, text=f"Saldo Akhir: {formatted_balance}", font=("Times New Roman", 16, "bold"), foreground="brown").pack(pady=10)

    global back_icon
    back_icon = resize_image("BACK.png",(50,50))
    ttk.Button(root, text="Kembali", image=back_icon, compound=tk.LEFT, command=show_main_menu).pack(pady=10)

# Menu utama
def show_main_menu():
    clear_frame()

    ttk.Label(root, text=f"Selamat Datang, {current_user['username']}", font=("Adventure Time Logo", 45), background="white").pack(pady=20)
    
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

# In your show_home function, replace the icon loading with:
def show_home():
    clear_frame()

    label = ttk.Label(root, text="Aplikasi Pengelolaan Uang", font=("Adventure Time Logo", 45), background='white', foreground='Black')
    label.pack(pady=20)

    global sign_up, sign_in
    sign_up = resize_image("SIGN UP.png", (70, 70))  
    sign_in = resize_image("SIGN IN.png", (70, 70))  

    ttk.Button(root, text="Sign Up", image=sign_up, compound=tk.LEFT, command=sign_up_user).place(relx=0.5, rely=0.4, anchor="center")
    ttk.Button(root, text="Sign In", image=sign_in, compound=tk.LEFT, command=sign_in_user).place(relx=0.5, rely=0.5, anchor="center")
    
# Memanggil fungsi untuk menampilkan GIF sebagai latar belakang
set_background_gif()

# Variabel pengguna
current_user = None

# Menampilkan halaman awal
show_home()

# Menjalankan aplikasi
root.mainloop()