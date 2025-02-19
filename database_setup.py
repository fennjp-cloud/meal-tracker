import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect("meal_tracker.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        weight REAL,
        meals TEXT,
        workout TEXT,
        macros TEXT,
        comments TEXT
    )
''')

conn.commit()
conn.close()

print("Database setup complete! ✅")
