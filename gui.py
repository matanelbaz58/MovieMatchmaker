import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import python_client

USER_EXIST = [1,2]
USER_DOES_NOT_EXIST = 0
USER_EXIST_AND_CORRECT_PASSWORD = 1
USER_EXIST_AND_INCORRECT_PASSWORD = 2


# Global variables
users_file = 'users.json'


def register():
    # Get the username and password from the entry fields
    username = new_username_entry.get()

    password = new_password_entry.get()

    rc = user_object.register_user(username, password)
    
    if rc == True:
            messagebox.showinfo("Success", "User registered successfully.")
            show_login_frame()
    
    else:
        messagebox.showerror("Error", "Failed to register user.")
        return

def login():
    # Get the username and password from the entry fields
    username = username_entry.get()
    password = password_entry.get()

    rc = user_object.login(username, password)   

    # Check if the username and password match
    if rc == USER_EXIST_AND_CORRECT_PASSWORD:
        messagebox.showinfo("Success", "Logged in successfully.")
        show_recommendation_frame()
    elif rc == USER_EXIST_AND_INCORRECT_PASSWORD:
        messagebox.showerror("Error", "Invalid username or password.")
    else:
        messagebox.showerror("Error", "User does not exist.")

def show_login_frame():
    # Hide other frames and show the login frame
    registration_frame.pack_forget()
    recommendation_frame.pack_forget()
    login_frame.pack()

def show_register_frame():
    # Hide other frames and show the registration frame
    login_frame.pack_forget()
    recommendation_frame.pack_forget()
    registration_frame.pack()

def show_recommendation_frame():
    # Hide other frames and show the recommendation frame
    login_frame.pack_forget()
    registration_frame.pack_forget()
    recommendation_frame.pack()

def submit():
    # Get the movie name and year from the entry fields and query the movie data
    movie_name = name_entry.get()
    movie_year = year_entry.get()
    user_object.user_input['year'] = movie_year

    query_movie_data(movie_name, movie_year)

def query_movie_data(name, year):
    # Print the movie name and year for querying
    print(user_object.make_api_call())# need to change. -----------------------------------------------------------

def setup_login_frame(root):
    # Create the login frame with entry fields for username and password
    global login_frame, username_entry, password_entry
    login_frame = ttk.Frame(root, padding="10 10 10 10")
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
    

def setup_registration_frame(root):
    # Create the registration frame with entry fields for new username and password
    global registration_frame, new_username_entry, new_password_entry
    registration_frame = ttk.Frame(root, padding="10 10 10 10")
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

def setup_recommendation_frame(root):
    # Create the recommendation frame with entry fields for movie name and year
    global recommendation_frame, name_entry, year_entry
    recommendation_frame = ttk.Frame(root, padding="10 10 10 10")
    ttk.Label(recommendation_frame, text="Movie Name:").grid(row=0, column=0)
    name_entry = ttk.Entry(recommendation_frame)
    name_entry.grid(row=0, column=1)
    ttk.Label(recommendation_frame, text="Year:").grid(row=1, column=0)
    year_entry = ttk.Entry(recommendation_frame)
    year_entry.grid(row=1, column=1)

    # New fields
    options = ["language", "region", "sort_by", "certification_country", "certification", 
               "certification.lte", "certification.gte", "include_adult", "page", 
               "release_date.gte", "release_date.lte", "watch_region", "with_cast", 
               "with_companies", "with_crew", "with_genres", "with_keywords", 
               "with_people", "with_runtime.gte", "with_runtime.lte", "without_companies", 
               "without_genres", "without_keywords", "year"]

    for i, option in enumerate(options, start=2):  # start from the 3rd row
        ttk.Label(recommendation_frame, text=f"{option}:").grid(row=i, column=0)
        entry = ttk.Entry(recommendation_frame)
        entry.grid(row=i, column=1)

    submit_button = ttk.Button(recommendation_frame, text="Submit", command=submit)
    submit_button.grid(row=len(options) + 2, column=0, columnspan=2)  # place the button after the last option

def main():
    # Create the main window and set up the frames
    global user_object
    user_object = python_client.Client(isMongoDBClient=True)
    root = tk.Tk()
    root.title("Movie Recommendation App")
    root.geometry("600x400")

    setup_login_frame(root)
    setup_registration_frame(root)
    setup_recommendation_frame(root)

    show_login_frame()
    root.mainloop()

if __name__ == "__main__":
    main()
