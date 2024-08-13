import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import python_client
import requests
from PIL import Image, ImageTk
from io import BytesIO

USER_EXIST = [1,2]
USER_DOES_NOT_EXIST = 0
USER_EXIST_AND_CORRECT_PASSWORD = 1
USER_EXIST_AND_INCORRECT_PASSWORD = 2


# Global variables
users_file = 'users.json'

def dropdown(name_field):
    # dropdown function
    return user_object.get_list_for_gui_dropdown(name_field)
       
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
    messagebox.showinfo("Success", "Logged in successfully.")
    show_recommendation_frame()
    return
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

def submit(entries):
    # Get the movie name and year from the entry fields and query the movie data
    get_movie_recommendations(entries)

def get_movie_recommendations(entries):
    # Collect all the fields from the entries dictionary
    params = {field: entry.get() for field, entry in entries.items() if entry.get()}
    
    # Print the collected parameters for debugging
    print("Query Parameters:", params)
    
    # Fetch movie recommendations using the collected parameters
    rc = user_object.get_movie_recommendations(params)
    
    if rc is None:
        messagebox.showerror("Error", "Failed to fetch movie recommendations.")
    else:
        messagebox.showinfo("Success", "Movie recommendations fetched successfully.")
        # Show the recommendations in a new window
        show_recommendations(rc)
        user_object.store_preference_to_history()
def show_photo_from_url(url):
    # Create a new window to display the movie image
    image_window = tk.Toplevel()
    image_window.title("Movie Image")

    # Fetch the image from the URL
    response = requests.get(url)
    image_data = response.content

    # Open the image using Pillow
    image = Image.open(BytesIO(image_data))

    # Convert the image to a format Tkinter can use
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    label = tk.Label(image_window, image=photo)
    label.image = photo  # Keep a reference to avoid garbage collection
    label.pack()

def show_recommendations(rc):
    # Create a new window to display the movie recommendations
    recommendations_window = tk.Toplevel()
    recommendations_window.title("Movie Recommendations")
    recommendations_window.geometry("400x300")

    # Display a list of movie titles
    if isinstance(rc, list) and len(rc) > 0:
        # save the number of movies
        num_movies = len(rc)
        print(f"Number of movies: {num_movies}")
        num_loops = 8 if num_movies >= 8 else num_movies
        for i, movie in enumerate(rc[:num_loops]):  
            movie_title = movie.get('title', 'Unknown Title')
            movie_image_url = movie.get('poster_url', None)

            # Display the movie title as a button
            button = ttk.Button(recommendations_window, text=f"{i+1}. {movie_title}", command=lambda url=movie_image_url: show_photo_from_url(url))
            button.pack(anchor='w', padx=10, pady=5)
       
    else:
        ttk.Label(recommendations_window, text="No recommendations available.").pack(anchor='center', padx=10, pady=10)


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
    # Create the recommendation frame
    global recommendation_frame
    recommendation_frame = ttk.Frame(root, padding="10 10 10 10")

    # New fields
    options = ["genre","language", "region", "sort_by", "certification_country", "certification", 
               "certification.lte", "certification.gte", "include_adult", "page", 
               "release_date.gte", "release_date.lte", "watch_region", "with_cast", 
               "with_companies", "with_crew", "with_genres", "with_keywords", 
               "with_people", "with_runtime.gte", "with_runtime.lte", "without_companies", 
               "without_genres", "without_keywords", "year"]

    entries = {}
    for i, option in enumerate(options):  # start from the 1st row
        ttk.Label(recommendation_frame, text=f"{option}:").grid(row=i, column=0)
        options_list = dropdown(option)
        combobox = ttk.Combobox(recommendation_frame, values=options_list)
        combobox.grid(row=i, column=1)
        entry = ttk.Entry(recommendation_frame)
        entries[option] = combobox

    submit_button = ttk.Button(recommendation_frame, text="Submit", command=lambda: submit(entries))
    submit_button.grid(row=len(options) + 1, column=0, columnspan=2)


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
