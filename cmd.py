import sqlite3

db_path = "/path/to/train.db"  # Replace with the correct path

try:
    import os
    # Resolve and set the absolute path to train.db
    db_path = os.path.abspath("train.db")
    if not os.path.exists(db_path):
       raise FileNotFoundError(f"Database file not found at {db_path}")
    print(f"Using database file at: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in train.db:", tables)
    
    # Check content of the examples table
    cursor.execute("SELECT * FROM examples LIMIT 5;")
    examples = cursor.fetchall()
    print("Sample examples:", examples)
    
    conn.close()
except Exception as e:
    print("Error reading train.db:", str(e))