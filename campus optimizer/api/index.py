from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import sqlite3
import pickle
import numpy as np
import os
import hashlib

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# Make session available in all templates
@app.context_processor
def inject_session():
    return {'session': session}

# Owner password for adding resources
OWNER_PASSWORD = "admin123"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    model = pickle.load(open(os.path.join(base_dir, "model.pkl"), "rb"))
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def connect_db():
    return sqlite3.connect(os.path.join(base_dir, "database.db"))


@app.route("/")
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")


@app.route("/resources")
def resources():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, status, capacity FROM resources")
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "name": row[1],
            "type": row[2],
            "status": row[3],
            "capacity": row[4]
        })

    return jsonify(data)


@app.route("/bookings")
def get_bookings():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, resource, user, timestamp FROM bookings ORDER BY timestamp DESC LIMIT 20")
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "resource": row[1],
            "user": row[2],
            "timestamp": row[3]
        })

    return jsonify(data)


@app.route("/book", methods=["POST"])
def book():
    resource = request.form.get("resource", "")
    user = request.form.get("user", "")

    if not resource or not user:
        return jsonify({"error": "Missing resource or user"}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO bookings (resource, user) VALUES (?, ?)",
        (resource, user)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": f"'{resource}' booked successfully by {user}!"})


@app.route("/predict")
def predict():
    if model is None:
        return jsonify({"error": "Model not available"}), 500
    time_val = request.args.get("time")
    if time_val is None:
        return jsonify({"error": "Missing time parameter"}), 400

    time_val = int(time_val)
    prediction = model.predict([[time_val]])
    usage = max(0, min(100, int(prediction[0])))

    if usage > 70:
        level = "High"
        suggestion = "Consider alternative rooms or come back later."
    elif usage > 40:
        level = "Medium"
        suggestion = "Some rooms may be available."
    else:
        level = "Low"
        suggestion = "Plenty of rooms available!"

    return jsonify({
        "predicted_usage": usage,
        "level": level,
        "suggestion": suggestion,
        "hour": time_val
    })


@app.route("/analytics")
def analytics():
    if model is None:
        return jsonify({"error": "Model not available"}), 500
    hours = list(range(1, 13))
    predictions = []
    for h in hours:
        pred = max(0, min(100, int(model.predict([[h]])[0])))
        predictions.append({"hour": h, "usage": pred})

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]
    cursor.execute("SELECT resource, COUNT(*) as cnt FROM bookings GROUP BY resource ORDER BY cnt DESC LIMIT 5")
    top_resources = [{"resource": row[0], "count": row[1]} for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        "hourly_predictions": predictions,
        "total_bookings": total_bookings,
        "top_resources": top_resources
    })


@app.route("/add-resource", methods=["POST"])
def add_resource():
    password = request.form.get("password", "")
    name = request.form.get("name", "").strip()
    rtype = request.form.get("type", "").strip()
    capacity = request.form.get("capacity", "")
    status = request.form.get("status", "available")

    # Check password
    if password != OWNER_PASSWORD:
        return jsonify({"error": "Invalid password"}), 403

    # Validate inputs
    if not name or not rtype or not capacity:
        return jsonify({"error": "All fields are required"}), 400

    try:
        capacity = int(capacity)
        if capacity <= 0:
            return jsonify({"error": "Capacity must be greater than 0"}), 400
    except ValueError:
        return jsonify({"error": "Capacity must be a number"}), 400

    # Add to database
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO resources (name, type, status, capacity) VALUES (?, ?, ?, ?)",
        (name, rtype, status, capacity)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "message": f"Resource '{name}' added successfully!",
        "success": True
    })


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode()).hexdigest()
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()
            conn.close()
            flash('Registered successfully! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = hashlib.sha256(password.encode()).hexdigest()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, hashed))
        row = cursor.fetchone()
        conn.close()
        if row:
            session['user'] = username
            session['role'] = row[0]
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    flash('Logged out successfully.')
    return redirect(url_for('home'))


@app.route('/books')
def books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, available FROM books WHERE block='AB1'")
    rows = cursor.fetchall()
    conn.close()
    total_available = sum(1 for row in rows if row[3])
    all_books = [{'id': row[0], 'title': row[1], 'author': row[2], 'available': row[3]} for row in rows]
    return render_template('books.html', total=total_available, books=all_books, is_owner=session.get('role') == 'owner')


@app.route('/upload_book', methods=['POST'])
def upload_book():
    if session.get('role') != 'owner':
        flash('Unauthorized access.')
        return redirect(url_for('home'))
    title = request.form['title']
    author = request.form['author']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    conn.close()
    flash('Book uploaded successfully.')
    return redirect(url_for('books'))


@app.route('/change_status', methods=['POST'])
def change_status():
    if session.get('role') != 'owner':
        flash('Unauthorized access.')
        return redirect(url_for('books'))
    book_id = request.form['book_id']
    available = int(request.form['available'])
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET available=? WHERE id=?", (available, book_id))
    conn.commit()
    conn.close()
    flash('Book status updated.')
    return redirect(url_for('books'))


@app.route('/delete_book', methods=['POST'])
def delete_book():
    if session.get('role') != 'owner':
        flash('Unauthorized access.')
        return redirect(url_for('books'))
    book_id = request.form['book_id']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    flash('Book deleted successfully.')
    return redirect(url_for('books'))


if __name__ == "__main__":
    app.run(debug=True)