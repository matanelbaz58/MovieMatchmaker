import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import python_client
import requests
from PIL import Image, ImageTk
from io import BytesIO
import webbrowser


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

    # Get the username and password from the entry fields
    username = "m"
    password = "m"

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
    # Get movie recommendations based on the user's input
    get_movie_recommendations(entries)

def recommendations_by_history(entries):
    # Get movie recommendations based on the history of the user
    get_movie_recommendations_by_histoy(entries)

def get_movie_recommendations_by_histoy(entries):
    # 
    rc = user_object.get_movie_recommendations_by_histoy()
    
    if rc is None:
        messagebox.showerror("Error", "Failed to fetch movie recommendations.")
    else:
        messagebox.showinfo("Success", "Movie recommendations fetched successfully.")
        # Show the recommendations in a new window
        show_recommendations(rc)
 

def get_movie_recommendations(entries):
    # Collect all the fields from the entries dictionary
    params = {field: entry.get() for field, entry in entries.items() if entry.get()}
    
    # Print the collected parameters for debugging
    print("Query Parameters:", params)
    
    # Fetch movie recommendations using the collected parameters
    if user_object.is_MongoDB_client():
        rc = user_object.get_movie_recommendations(params) 
    else:
        rc, tx_hash_link = user_object.get_movie_recommendations(params) # tx

    if rc is None:
        messagebox.showerror("Error", "Failed to fetch movie recommendations.")
    else:
        messagebox.showinfo("Success", "Movie recommendations fetched successfully.")
        # Show the recommendations in a new window
        if user_object.is_MongoDB_client():
            show_recommendations(rc)
        else:
            show_recommendations(rc,tx_hash_link)

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

def open_movie_info(movie):
    if movie:
        # Extract the title from the movie dictionary
        title = movie.get('title', 'Unknown Title')
        # Extract other relevant information if needed
        overview = movie.get('overview', 'No description available.')
        release_date = movie.get('release_date', 'Unknown release date')
        
        # Create a new window to display the movie information
        info_window = tk.Toplevel()
        info_window.title(f"Movie Info: {title}")
        info_window.geometry("400x300")
        
        # Display the movie information in the window
        ttk.Label(info_window, text=f"Title: {title}", font=("Helvetica", 14, "bold")).pack(anchor='w', padx=10, pady=5)
        ttk.Label(info_window, text=f"Overview: {overview}", wraplength=380).pack(anchor='w', padx=10, pady=5)
        ttk.Label(info_window, text=f"Release Date: {release_date}").pack(anchor='w', padx=10, pady=5)
        
        # Optionally, you can add more details or styling as needed
        
    else:
        print("Invalid movie data: None")
        
def show_recommendations(rc,tx_hash_link=None):
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
            movie_info_url = movie.get('info_url', None)  # Assuming 'info_url' is the key for the movie information URL

            # Display the movie title as a button
            button = ttk.Button(recommendations_window, text=f"{i+1}. {movie_title}", command=lambda url=movie_image_url: show_photo_from_url(url))
            button.pack(anchor='w', padx=10, pady=5)

            # Display the movie information link as a button
            info_button = ttk.Button(recommendations_window, text="More Info", command=lambda movie=movie: open_movie_info(movie))
            info_button.pack(anchor='w', padx=10, pady=5)
       
    else:
        ttk.Label(recommendations_window, text="No recommendations available.").pack(anchor='center', padx=10, pady=10)
    
    # Add a button for tx_hash_link if provided
    if tx_hash_link:
        tx_button = ttk.Button(recommendations_window, text="Transaction Link", command=lambda: open_tx_link(tx_hash_link))
        tx_button.pack(anchor='center', padx=10, pady=10)

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
    
    recommendations_by_history_button = ttk.Button(recommendation_frame, text="Recommendations by History", command=lambda: recommendations_by_history(entries))
    recommendations_by_history_button.grid(row=len(options) + 2, column=0, columnspan=2)

def main():
    # Create the main window and set up the frames
    global user_object
    user_object = python_client.Client(is_mongo_db_client=True)
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
