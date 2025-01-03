import csv
import os
import hashlib

USER_FILE = "users.csv"

def initialize_user_file():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "username", "password", "email"])

initialize_user_file()

def read_users():
    with open(USER_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)  

def write_users(users):
    with open(USER_FILE, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "username", "password", "email"])
        writer.writeheader()  
        writer.writerows(users) 

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def hash_existing_passwords():
    users = read_users()  
    for user in users:
        if len(user["password"]) < 64:
            user["password"] = hash_password(user["password"])
    write_users(users) 
    print("Semua password telah di-hash.")

def sign_up(username, password, email):
    users = read_users()  
    if any(user["username"] == username for user in users):
        return "Username sudah terdaftar."

    if any(user["email"] == email for user in users):
        return "Email sudah terdaftar."

    user_id = len(users) + 1  
    users.append({
        "id": user_id,
        "username": username,
        "password": hash_password(password),  
        "email": email
    })
    write_users(users)  
    return "Registrasi berhasil!"

def sign_in(username, password):
    users = read_users()  
    for user in users:
        if user["username"] == username:
            if user["password"] == hash_password(password): 
                return user  
            else:
                return "Kata sandi salah."
    return "Username tidak ditemukan."

def get_all_users():
    return read_users()

hash_existing_passwords()
