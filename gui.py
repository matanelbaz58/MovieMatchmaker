import tkinter as tk
from tkinter import ttk

# Function to update the start year label
def update_start_year_label(value):
    start_year_label.config(text=f"Start Year: {int(float(value))}")

# Function to update the end year label
def update_end_year_label(value):
    end_year_label.config(text=f"End Year: {int(float(value))}")

# Function to simulate sending data to an API
def submit():
    movie_name = name_entry.get()
    selected_genres = [genre for genre, var in genres.items() if var.get() == 1]
    start_year = int(start_year_scale.get())
    end_year = int(end_year_scale.get())
    rating_preference = rating_var.get()
    print(f"Movie Name: {movie_name}, Genres: {selected_genres}, Year Range: {start_year}-{end_year}, Rating: {rating_preference}")
    # Here, replace the print statement with your API call logic for movie recommendations

# Create the main window
root = tk.Tk()
root.title("Movie Recommendation App")
root.geometry("600x400")

# Create and grid the layout frames
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Movie Name Entry
ttk.Label(main_frame, text="Movie Name (optional):").grid(column=0, row=0, sticky=tk.W)
name_entry = ttk.Entry(main_frame, width=30)
name_entry.grid(column=1, row=0, sticky=tk.W)

# Genre Selection
ttk.Label(main_frame, text="Preferred Genres:").grid(column=0, row=1, sticky=tk.W, pady=5)
genres_frame = ttk.Frame(main_frame)
genres_frame.grid(column=1, row=1, sticky=tk.W)
genres = {"Action": tk.IntVar(), "Comedy": tk.IntVar(), "Drama": tk.IntVar(), "Fantasy": tk.IntVar(), "Horror": tk.IntVar()}
for i, (genre, var) in enumerate(genres.items()):
    ttk.Checkbutton(genres_frame, text=genre, variable=var).grid(column=i, row=1, sticky=tk.W)

# Start Year Slider and Label
start_year_label = ttk.Label(main_frame, text="Start Year:")
start_year_label.grid(column=0, row=2, sticky=tk.W, pady=5)
start_year_scale = ttk.Scale(main_frame, from_=1900, to=2024, orient=tk.HORIZONTAL, length=200, command=update_start_year_label)
start_year_scale.set(1900)  # set to default/start value
start_year_scale.grid(column=1, row=2, sticky=tk.W)

# End Year Slider and Label
end_year_label = ttk.Label(main_frame, text="End Year:")
end_year_label.grid(column=0, row=3, sticky=tk.W, pady=5)
end_year_scale = ttk.Scale(main_frame, from_=1900, to=2024, orient=tk.HORIZONTAL, length=200, command=update_end_year_label)
end_year_scale.set(2024)  # set to default/end value
end_year_scale.grid(column=1, row=3, sticky=tk.W)

# Rating Preference Dropdown
ttk.Label(main_frame, text="Rating Preference:").grid(column=0, row=4, sticky=tk.W, pady=5)
rating_var = tk.StringVar()
rating_dropdown = ttk.Combobox(main_frame, textvariable=rating_var, state="readonly")
rating_dropdown['values'] = ("Any", "G", "PG", "PG-13", "R", "NC-17")
rating_dropdown.current(0)
rating_dropdown.grid(column=1, row=4, sticky=tk.W)

# Submit Button
submit_button = ttk.Button(main_frame, text="Get Recommendations", command=submit)
submit_button.grid(column=1, row=5, sticky=tk.W, pady=10)

# Initial call to update labels
update_start_year_label(start_year_scale.get())
update_end_year_label(end_year_scale.get())
root.mainloop()