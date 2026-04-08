import os
import subprocess
import socket
from app import app

# Check if model.pkl exists, if not, train the model
if not os.path.exists('model.pkl'):
    print("Training model...")
    subprocess.run(['python', 'model.py'])

# Check if database.db exists, if not, set up the database
if not os.path.exists('database.db'):
    print("Setting up database...")
    subprocess.run(['python', 'setup_db.py'])

if __name__ == '__main__':
    print("Starting the Flask app...")
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Access the app at: http://{local_ip}:5000")
    app.run(host='0.0.0.0', debug=True)