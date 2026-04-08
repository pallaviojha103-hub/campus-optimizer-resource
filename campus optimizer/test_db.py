import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:", [row[0] for row in tables])

# Check books
cursor.execute("SELECT * FROM books")
books = cursor.fetchall()
print(f"\nBooks found: {len(books)}")
for book in books:
    print(book)

conn.close()
