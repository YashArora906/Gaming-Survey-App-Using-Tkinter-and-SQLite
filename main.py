import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create SQLite database and tables
conn = sqlite3.connect('gaming_survey.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS survey_responses (
                    name TEXT,
                    age_group TEXT,
                    devices TEXT,
                    game_types TEXT,
                    graphics_importance INTEGER,
                    gaming_time INTEGER,
                    preferred_genre TEXT,
                    multiplayer_preference TEXT,
                    preferred_difficulty TEXT)''')
conn.commit()

# Function to handle login
def login():
    username = login_username_entry.get()
    password = login_password_entry.get()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if cursor.fetchone():
        messagebox.showinfo("Login Successful", "Welcome to the Gaming Survey!")
        show_survey_form()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to handle signup
def signup():
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    if username and password:
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Signup Failed", "Username already exists.")
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Signup Successful", "Account created. Please log in.")
            show_login_form()
    else:
        messagebox.showerror("Signup Failed", "Please fill in all fields.")

# Function to handle survey submission
def submit_survey():
    name = name_entry.get()
    age_group = age_var.get()
    devices = ', '.join([device for device, var in device_vars.items() if var.get()])
    game_types = ', '.join([game for game, var in game_vars.items() if var.get()])
    graphics_importance = graphics_scale.get()
    gaming_time = gaming_time_entry.get()
    preferred_genre = preferred_genre_entry.get()
    multiplayer_preference = multiplayer_var.get()
    preferred_difficulty = difficulty_var.get()

    if not gaming_time.isdigit():
        messagebox.showerror("Invalid Input", "Please enter a valid number for gaming time.")
        return

    cursor.execute('''INSERT INTO survey_responses (name, age_group, devices, game_types, graphics_importance, gaming_time, preferred_genre, multiplayer_preference, preferred_difficulty)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (name, age_group, devices, game_types, graphics_importance, int(gaming_time), preferred_genre, multiplayer_preference, preferred_difficulty))
    conn.commit()
    messagebox.showinfo("Submitted", "Thank you for your responses!")

# Function to show login form
def show_login_form():
    signup_frame.pack_forget()
    survey_frame.pack_forget()
    visualization_frame.pack_forget()
    login_frame.pack(pady=5)

# Function to show signup form
def show_signup_form():
    login_frame.pack_forget()
    survey_frame.pack_forget()
    visualization_frame.pack_forget()
    signup_frame.pack(pady=5)

# Function to show survey form
def show_survey_form():
    login_frame.pack_forget()
    signup_frame.pack_forget()
    visualization_frame.pack_forget()
    survey_frame.pack(pady=5)

# Function to show visualizations
def show_visualizations():
    login_frame.pack_forget()
    signup_frame.pack_forget()
    survey_frame.pack_forget()
    visualization_frame.pack(pady=5)

# Visualization functions
def plot_age_gender_distribution():
    file_path = 'Data.csv'
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()

    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.countplot(data=data, x='Age', hue='Gender', palette='viridis')
    plt.title("Age and Gender Distribution")
    plt.xlabel("Age Group")
    plt.ylabel("Count")
    plt.legend(title="Gender")
    plt.show()

def plot_preferred_devices():
    file_path = 'Data.csv'
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()

    preferred_devices = data['What type of gaming devices do you prefer?'].str.get_dummies(sep=', ').sum()
    preferred_devices.sort_values(ascending=False, inplace=True)

    plt.figure(figsize=(8, 5))
    preferred_devices.plot(kind='barh', color='skyblue')
    plt.title("Preferred Gaming Devices (Unique Count per Device)")
    plt.xlabel("Count")
    plt.ylabel("Device Type")
    plt.show()

def plot_favorite_games():
    file_path = 'Data.csv'
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()

    favorite_games = data['What are your favorite types of games?'].str.get_dummies(sep=', ').sum()
    favorite_games.sort_values(ascending=False, inplace=True)

    plt.figure(figsize=(8, 5))
    favorite_games.plot(kind='bar', color='skyblue')
    plt.title("Favorite Game Types")
    plt.xlabel("Game Type")
    plt.ylabel("Count")
    plt.show()

def plot_free_time_spent_on_gaming():
    file_path = 'Data.csv'
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()

    free_time_counts = data['What percentage of your free time is spent on gaming?'].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(free_time_counts, labels=free_time_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("bright"))
    plt.title("Percentage of Free Time Spent on Gaming")
    plt.show()

def plot_graphics_importance_by_age_group():
    file_path = 'Data.csv'
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()

    # Box plot: Importance of Graphics by Age Group
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data, x='Age', y='How important are graphics and visuals to your gaming experience?', palette='Set3')
    plt.title("Importance of Graphics by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Importance of Graphics (1-10)")
    plt.show()

# Initialize main Tkinter window
root = tk.Tk()
root.title("Gaming Survey")
root.geometry("350x700")
root.configure(bg="#f7f7f7")

LABEL_STYLE = {"font": ("Arial", 10), "bg": "#f7f7f7", "anchor": "w"}
ENTRY_STYLE = {"width": 25}

# Login Frame
login_frame = tk.Frame(root, bg="#f7f7f7")
tk.Label(login_frame, text="Login", font=("Arial", 14), bg="#f7f7f7").pack(pady=5)
tk.Label(login_frame, text="Username:", **LABEL_STYLE).pack()
login_username_entry = tk.Entry(login_frame, **ENTRY_STYLE)
login_username_entry.pack()
tk.Label(login_frame, text="Password:", **LABEL_STYLE).pack()
login_password_entry = tk.Entry(login_frame, show="*", **ENTRY_STYLE)
login_password_entry.pack()
tk.Button(login_frame, text="Login", command=login, bg="#4CAF50", fg="white", width=20).pack(pady=5)
tk.Button(login_frame, text="Sign Up", command=show_signup_form, bg="#dddddd", width=20).pack()
tk.Button(login_frame, text="View Visualizations", command=show_visualizations, bg="#dddddd", width=20).pack()

# Signup Frame
signup_frame = tk.Frame(root, bg="#f7f7f7")
tk.Label(signup_frame, text="Sign Up", font=("Arial", 14), bg="#f7f7f7").pack(pady=5)
tk.Label(signup_frame, text="Username:", **LABEL_STYLE).pack()
signup_username_entry = tk.Entry(signup_frame, **ENTRY_STYLE)
signup_username_entry.pack()
tk.Label(signup_frame, text="Password:", **LABEL_STYLE).pack()
signup_password_entry = tk.Entry(signup_frame, show="*", **ENTRY_STYLE)
signup_password_entry.pack()
tk.Button(signup_frame, text="Sign Up", command=signup, bg="#4CAF50", fg="white", width=20).pack(pady=5)
tk.Button(signup_frame, text="Back to Login", command=show_login_form, bg="#dddddd", width=20).pack()
tk.Button(signup_frame, text="View Visualizations", command=show_visualizations, bg="#dddddd", width=20).pack()

# Survey Frame
survey_frame = tk.Frame(root, bg="#f7f7f7")
tk.Label(survey_frame, text="Gaming Survey", font=("Arial", 14), bg="#f7f7f7").pack(pady=5)
tk.Label(survey_frame, text="Name:", **LABEL_STYLE).pack()
name_entry = tk.Entry(survey_frame, **ENTRY_STYLE)
name_entry.pack()
tk.Label(survey_frame, text="Age Group:", **LABEL_STYLE).pack()
age_var = tk.StringVar(value="18-22")
age_options = ["Under 18", "18-22", "23-35", "35+"]
for age in age_options:
    tk.Radiobutton(survey_frame, text=age, variable=age_var, value=age, **LABEL_STYLE).pack(anchor="w")
tk.Label(survey_frame, text="What type of gaming devices do you prefer?", **LABEL_STYLE).pack()
device_vars = {"PC": tk.BooleanVar(), "Console": tk.BooleanVar(), "Mobile": tk.BooleanVar()}
for device in device_vars:
    tk.Checkbutton(survey_frame, text=device, variable=device_vars[device], **LABEL_STYLE).pack(anchor="w")
tk.Label(survey_frame, text="What are your favorite types of games?", **LABEL_STYLE).pack()
game_vars = {"Action": tk.BooleanVar(), "RPG": tk.BooleanVar(), "Sports": tk.BooleanVar(), "Strategy": tk.BooleanVar()}
for game in game_vars:
    tk.Checkbutton(survey_frame, text=game, variable=game_vars[game], **LABEL_STYLE).pack(anchor="w")
tk.Label(survey_frame, text="How important are graphics and visuals to your gaming experience?", **LABEL_STYLE).pack()
graphics_scale = tk.Scale(survey_frame, from_=1, to=10, orient="horizontal", **ENTRY_STYLE)
graphics_scale.pack()
tk.Label(survey_frame, text="How many hours do you spend gaming per week?", **LABEL_STYLE).pack()
gaming_time_entry = tk.Entry(survey_frame, **ENTRY_STYLE)
gaming_time_entry.pack()
tk.Label(survey_frame, text="What is your preferred game genre?", **LABEL_STYLE).pack()
preferred_genre_entry = tk.Entry(survey_frame, **ENTRY_STYLE)
preferred_genre_entry.pack()
tk.Label(survey_frame, text="Multiplayer preference:", **LABEL_STYLE).pack()
multiplayer_var = tk.StringVar(value="Yes")
tk.Radiobutton(survey_frame, text="Yes", variable=multiplayer_var, value="Yes", **LABEL_STYLE).pack(anchor="w")
tk.Radiobutton(survey_frame, text="No", variable=multiplayer_var, value="No", **LABEL_STYLE).pack(anchor="w")
tk.Label(survey_frame, text="Preferred difficulty:", **LABEL_STYLE).pack()
difficulty_var = tk.StringVar(value="Normal")
difficulty_options = ["Easy", "Normal", "Hard"]
for difficulty in difficulty_options:
    tk.Radiobutton(survey_frame, text=difficulty, variable=difficulty_var, value=difficulty, **LABEL_STYLE).pack(anchor="w")
tk.Button(survey_frame, text="Submit Survey", command=submit_survey, bg="#4CAF50", fg="white", width=20).pack(pady=5)
tk.Button(survey_frame, text="Back to Login", command=show_login_form, bg="#dddddd", width=20).pack()

# Visualization Frame
visualization_frame = tk.Frame(root, bg="#f7f7f7")
tk.Button(visualization_frame, text="Age & Gender Distribution", command=plot_age_gender_distribution, bg="#4CAF50", fg="white", width=30).pack(pady=5)
tk.Button(visualization_frame, text="Preferred Devices", command=plot_preferred_devices, bg="#4CAF50", fg="white", width=30).pack(pady=5)
tk.Button(visualization_frame, text="Favorite Game Types", command=plot_favorite_games, bg="#4CAF50", fg="white", width=30).pack(pady=5)
tk.Button(visualization_frame, text="Gaming Time Distribution", command=plot_free_time_spent_on_gaming, bg="#4CAF50", fg="white", width=30).pack(pady=5)
tk.Button(visualization_frame, text="Graphics Importance by Age", command=plot_graphics_importance_by_age_group, bg="#4CAF50", fg="white", width=30).pack(pady=5)
tk.Button(visualization_frame, text="Back to Login", command=show_login_form, bg="#dddddd", width=20).pack()

# Show login form initially
show_login_form()

# Run the application
root.mainloop()
