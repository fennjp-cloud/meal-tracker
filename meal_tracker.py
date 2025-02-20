import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, ttk as tk

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

    cursor.execute("SELECT id, date, weight FROM logs ORDER BY date DESC")
    rows = cursor.fetchall()

    for row in rows:
        log_id, date, weight = row
        tree.insert("", "end", values=(log_id, date, weight, "🔍 View"), tags=("clickable",))

# Function to show full log details in a new window
def view_entry(event):
    selected_item = tree.selection()
    if not selected_item:
        return

    item = tree.item(selected_item)
    log_id = item['values'][0]

    cursor.execute("SELECT * FROM logs WHERE id=?", (log_id,))
    log_data = cursor.fetchone()

    if not log_data:
        return

    # Extract full log details
    _, date, weight, meals, workout, macros, comments = log_data

    # Create a new window for viewing full details
    detail_window = ttk.Toplevel(root)
    detail_window.title(f"Log Details - {date}")
    detail_window.geometry("500x400")

    ttk.Label(detail_window, text=f"📅 Date: {date}", font=("Helvetica", 12, "bold")).pack(pady=5)
    ttk.Label(detail_window, text=f"⚖️ Weight: {weight} lbs", font=("Helvetica", 10)).pack(pady=5)

    ttk.Label(detail_window, text="🍽️ Meals:", font=("Helvetica", 10, "bold")).pack(anchor="w", padx=10)
    ttk.Label(detail_window, text=meals, wraplength=450, justify="left").pack(anchor="w", padx=10, pady=2)

    ttk.Label(detail_window, text="🏋️ Workout:", font=("Helvetica", 10, "bold")).pack(anchor="w", padx=10)
    ttk.Label(detail_window, text=workout, wraplength=450, justify="left").pack(anchor="w", padx=10, pady=2)

    ttk.Label(detail_window, text="💪 Macros:", font=("Helvetica", 10, "bold")).pack(anchor="w", padx=10)
    ttk.Label(detail_window, text=macros, wraplength=450, justify="left").pack(anchor="w", padx=10, pady=2)

    ttk.Label(detail_window, text="📝 Comments:", font=("Helvetica", 10, "bold")).pack(anchor="w", padx=10)
    ttk.Label(detail_window, text=comments, wraplength=450, justify="left").pack(anchor="w", padx=10, pady=2)

    ttk.Button(detail_window, text="Close", bootstyle="danger", command=detail_window.destroy).pack(pady=10)

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
    import pandas as pd
    df = pd.DataFrame(rows, columns=["ID", "Date", "Weight", "Meals", "Workout", "Macros", "Comments"])
    df.to_csv("meal_tracker.csv", index=False)
    messagebox.showinfo("Export", "Data exported to meal_tracker.csv")

# GUI Setup
root = ttk.Window(themename="superhero")  # Dark Mode Theme
root.title("Meal & Workout Tracker")
root.geometry("900x600")
root.resizable(True, True)

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
ttk.Label(form_frame, text="Workout:").grid(row=2, column=0, padx=5, pady=5)
workout_entry = ttk.Text(form_frame, height=3, width=40)
workout_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

# Macros Input
ttk.Label(form_frame, text="Macros:").grid(row=3, column=0, padx=5, pady=5)
macros_entry = ttk.Text(form_frame, height=3, width=40)
macros_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5)

# Comments Input
ttk.Label(form_frame, text="Comments:").grid(row=4, column=0, padx=5, pady=5)
comments_entry = ttk.Text(form_frame, height=3, width=40)
comments_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

# Buttons
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Log Entry", bootstyle="success", command=log_entry).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Export CSV", bootstyle="info", command=export_csv).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="Delete Entry", bootstyle="danger", command=delete_entry).grid(row=0, column=2, padx=10)

# Display Entries Table
columns = ("ID", "Date", "Weight", "View")
tree = tk.Treeview(main_frame, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Bind Click Event
tree.bind("<Double-1>", view_entry)

fetch_entries()

root.mainloop()

# Close database connection on exit
conn.close()
