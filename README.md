# 🏫 SmartCampus Resource Optimizer

A smart web-based system designed to **efficiently manage and optimize campus resources** like labs, study rooms, and shared spaces using real-time data and predictive analytics.

---

## 🚀 Features

✨ **Real-Time Availability**  
View available labs and study rooms instantly.

📅 **Smart Booking System**  
Book resources seamlessly with a simple interface.

🧠 **AI-Based Usage Prediction**  
Predict future resource usage using a machine learning model.

📊 **Usage Analytics**  
Understand peak usage hours and optimize scheduling.

🎨 **Clean Dashboard UI**  
Minimal and intuitive interface for better user experience.

---

💡 Problem It Solves

Campus resources are often:

Underutilized
Overbooked
Poorly managed

This system introduces data-driven decision making to maximize efficiency and accessibility.

---

## 🧠 How It Works

This project combines **web development + machine learning**:

- A **Linear Regression model** predicts resource usage based on time.
- A **Flask backend** handles API requests and booking logic.
- A **SQLite database** stores resources and booking data.
- A simple **frontend UI** allows users to interact with the system.

---

## 🛠️ Tech Stack

| Layer       | Technology Used        |
|------------|----------------------|
| Frontend    | HTML, JavaScript     |
| Backend     | Flask (Python)       |
| Database    | SQLite               |
| ML Model    | Scikit-learn         |
| Hosting     | Replit (or local)    |

---

## 📁 Project Structure
campus-resource-optimizer/
│
├── app.py # Flask backend
├── model.py # ML prediction model
├── model.pkl # Trained model file
├── database.db # SQLite database
├── templates/
│ └── index.html # Frontend UI
└── requirements.txt


---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/campus-resource-optimizer.git
cd campus-resource-optimizer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the Model
```bash
python model.py
```

### 4. Setup Database (Run Once)
Open Python and run:

``` bash
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE resources(
id INTEGER PRIMARY KEY,
name TEXT
)
""")

cursor.execute("""
CREATE TABLE bookings(
id INTEGER PRIMARY KEY,
resource TEXT,
user TEXT
)
""")

cursor.execute("INSERT INTO resources (name) VALUES ('Lab 1')")
cursor.execute("INSERT INTO resources (name) VALUES ('Study Room A')")
cursor.execute("INSERT INTO resources (name) VALUES ('Library Hall')")

conn.commit()
conn.close()
```
### 5. Run the App
```bash
python app.py
```

### Visit:
http://127.0.0.1:5000

## 📡 API Endpoints

| Endpoint      | Method | Description              |
|--------------|--------|--------------------------|
| `/`          | GET    | Load homepage           |
| `/resources` | GET    | Fetch all resources     |
| `/book`      | POST   | Book a resource         |
| `/predict`   | GET    | Predict usage           |

---

### 🤖 Machine Learning Model
Algorithm: Linear Regression
Input: Time of day
Output: Predicted usage level

This helps in:

Avoiding peak-time bookings
Improving resource allocation
Enhancing user experience

---

### Screenshots

![WhatsApp Image 2026-04-08 at 2 15 32 PM](https://github.com/user-attachments/assets/c1980839-10ec-4da9-872a-32b56e65f8d3)

### 🌟 Future Improvements
🔔 Notification system for bookings
📱 Mobile-friendly UI
🔐 User authentication system
📊 Advanced analytics dashboard
🤖 Smarter ML models for better prediction

---

### 👩‍💻 Author

## Team Vibrathon
Members:
- Shreya Adhikary (25BCE11282)
- Aryan Kumar (25BCE10362)
- Paridhi Agrawal (25BCE11192)
- Pallavi Kumari (25BAI10352)

---





