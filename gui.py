import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

# Define paths for user file
users_file = 'users.json'

# Function to load users from JSON
def load_users():
    if not os.path.exists(users_file):
        with open(users_file, 'w') as file:
            json.dump({}, file)
    with open(users_file, 'r') as file:
        return json.load(file)

# Function to save users to JSON
def save_users(users):
    with open(users_file, 'w') as file:
        json.dump(users, file, indent=4)

# Function to register a new user
def register():
    username = new_username_entry.get()
    password = new_password_entry.get()
    users = load_users()

    if username in users:
        messagebox.showerror("Error", "User already exists.")
        return

    users[username] = password
    save_users(users)
    messagebox.showinfo("Success", "User registered successfully.")
    show_login_frame()

# Function to login a user
def login():
    username = username_entry.get()
    password = password_entry.get()
    users = load_users()

    if users.get(username) == password:
        messagebox.showinfo("Success", "Logged in successfully.")
        show_recommendation_frame()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Function to show login frame
def show_login_frame():
    registration_frame.pack_forget()
    recommendation_frame.pack_forget()
    login_frame.pack()

# Function to show register frame
def show_register_frame():
    login_frame.pack_forget()
    recommendation_frame.pack_forget()
    registration_frame.pack()

# Function to show recommendation frame
def show_recommendation_frame():
    login_frame.pack_forget()
    registration_frame.pack_forget()
    recommendation_frame.pack()

# Function to submit recommendation request
def submit():
    movie_name = name_entry.get()
    # ... your existing submit logic ...
    print(f"Movie Name: {movie_name}")
    # ... your existing submit logic ...

root = tk.Tk()
root.title("Movie Recommendation App")
root.geometry("600x400")

# Frames for each section of the application
login_frame = ttk.Frame(root, padding="10 10 10 10")
registration_frame = ttk.Frame(root, padding="10 10 10 10")
recommendation_frame = ttk.Frame(root, padding="10 10 10 10")

# Building the login frame
ttk.Label(login_frame, text="Username:").pack()
username_entry = ttk.Entry(login_frame)
username_entry.pack()
ttk.Label(login_frame, text="Password:").pack()
password_entry = ttk.Entry(login_frame, show='*')
password_entry.pack()
login_button = ttk.Button(login_frame, text="Login", command=login)
login_button.pack()
register_button = ttk.Button(login_frame, text="Register", command=show_register_frame)
register_button.pack()

# Building the registration frame
ttk.Label(registration_frame, text="Choose a Username:").pack()
new_username_entry = ttk.Entry(registration_frame)
new_username_entry.pack()
ttk.Label(registration_frame, text="Choose a Password:").pack()
new_password_entry = ttk.Entry(registration_frame, show='*')
new_password_entry.pack()
register_new_button = ttk.Button(registration_frame, text="Register", command=register)
register_new_button.pack()
back_to_login_button = ttk.Button(registration_frame, text="Back to Login", command=show_login_frame)
back_to_login_button.pack()

# Building the recommendation frame
ttk.Label(recommendation_frame, text="Movie Name:").pack()
name_entry = ttk.Entry(recommendation_frame)
name_entry.pack()
submit_button = ttk.Button(recommendation_frame, text="Submit", command=submit)
submit_button.pack()

# Pack the initial login frame
show_login_frame()

root.mainloop()
