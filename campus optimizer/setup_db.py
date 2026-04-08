import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

# Remove old DB if exists
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE resources(
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    status TEXT DEFAULT 'available',
    capacity INTEGER DEFAULT 30
)
""")

cursor.execute("""
CREATE TABLE bookings(
    id INTEGER PRIMARY KEY,
    resource TEXT,
    user TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Seed data
resources = [
    ('Lab 1', 'Laboratory', 'available', 40),
    ('Lab 2', 'Laboratory', 'occupied', 35),
    ('Study Room A', 'Study Room', 'available', 20),
    ('Study Room B', 'Study Room', 'occupied', 15),
    ('Library Hall', 'Library', 'available', 100),
    ('Computer Lab', 'Laboratory', 'available', 50),
    ('Seminar Hall', 'Hall', 'occupied', 80),
    ('Reading Room', 'Library', 'available', 25),
]

for name, rtype, status, cap in resources:
    cursor.execute(
        "INSERT INTO resources (name, type, status, capacity) VALUES (?,?,?,?)",
        (name, rtype, status, cap)
    )

cursor.execute("""
CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'student'
)
""")

cursor.execute("""
CREATE TABLE books(
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    available INTEGER DEFAULT 1,
    block TEXT DEFAULT 'AB1'
)
""")

# Seed books
books = [
    ('Introduction to Algorithms', 'Cormen', 1, 'AB1'),
    ('Data Structures and Algorithms', 'Goodrich', 1, 'AB1'),
    ('Computer Networks', 'Tanenbaum', 0, 'AB1'),
    ('Operating Systems', 'Silberschatz', 1, 'AB1'),
    ('Database System Concepts', 'Silberschatz', 1, 'AB1'),
]

for title, author, avail, block in books:
    cursor.execute(
        "INSERT INTO books (title, author, available, block) VALUES (?,?,?,?)",
        (title, author, avail, block)
    )

# Seed owner user
import hashlib
owner_password = hashlib.sha256("admin123".encode()).hexdigest()
cursor.execute(
    "INSERT INTO users (username, password, role) VALUES (?,?,?)",
    ('owner', owner_password, 'owner')
)

conn.commit()
conn.close()

print("Database initialized successfully!")
