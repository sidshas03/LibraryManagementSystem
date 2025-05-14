import sqlite3

DB_NAME = 'library.db'

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Check if 'icon' column exists
cursor.execute("PRAGMA table_info(books)")
columns = [col[1] for col in cursor.fetchall()]

if 'icon' not in columns:
    cursor.execute('ALTER TABLE books ADD COLUMN icon TEXT')
    print("'icon' column added to books table.")
else:
    print("'icon' column already exists.")

conn.commit()
conn.close() 