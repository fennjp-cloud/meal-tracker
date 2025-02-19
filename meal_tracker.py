import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("meal_tracker.db")
cursor = conn.cursor()

# Function to log an entry
def log_entry():
    date = date_entry.get()
    weight = weight_entry.get()
    meals = meals_entry.get("1.0", "end").strip()
    workout = workout_entry.get("1.0", "end").strip()
    macros = macros_entry.get("1.0", "end").strip()
    comments = comments_entry.get("1.0", "end").strip()

    if not date or not meals:
        messagebox.showerror("Error", "Date and Meals are required!")
        return
    
    cursor.execute("INSERT INTO logs (date, weight, meals, workout, macros, comments) VALUES (?, ?, ?, ?, ?, ?)",
                   (date, weight, meals, workout, macros, comments))
    conn.commit()
    messagebox.showinfo("Success", "Entry logged successfully!")
    fetch_entries()

# Function to fetch and display entries
def fetch_entries():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM logs ORDER BY date DESC")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

# Function to delete an entry
def delete_entry():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an entry to delete.")
        return
    item = tree.item(selected_item)
    log_id = item['values'][0]
    
    cursor.execute("DELETE FROM logs WHERE id=?", (log_id,))
    conn.commit()
    fetch_entries()
    messagebox.showinfo("Success", "Entry deleted!")

# Function to export data to CSV
def export_csv():
    cursor.execute("SELECT * FROM logs")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Date", "Weight", "Meals", "Workout", "Macros", "Comments"])
    df.to_csv("meal_tracker.csv", index=False)
    messagebox.showinfo("Export", "Data exported to meal_tracker.csv")

# GUI Setup
root = ttk.Window(themename="superhero")  # Modern Dark Mode Theme
root.title("Meal & Workout Tracker")
root.geometry("800x600")
root.resizable(False, False)

# Main Frame
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill=BOTH, expand=True)

# Header
title_label = ttk.Label(main_frame, text="Meal & Workout Tracker", font=("Helvetica", 18, "bold"), bootstyle="primary")
title_label.pack(pady=10)

# Input Fields
form_frame = ttk.Frame(main_frame)
form_frame.pack(fill=X, padx=10)

ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
date_entry = ttk.Entry(form_frame, width=20)
date_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(form_frame, text="Weight (lbs):").grid(row=0, column=2, padx=5, pady=5)
weight_entry = ttk.Entry(form_frame, width=10)
weight_entry.grid(row=0, column=3, padx=5, pady=5)

# Meals Input
ttk.Label(form_frame, text="Meals:").grid(row=1, column=0, padx=5, pady=5)
meals_entry = ttk.Text(form_frame, height=3, width=40)
meals_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

# Workout Input
ttk.Label(form_frame, text="Workout:").grid
