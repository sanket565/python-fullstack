# 🚀 User Management Web Application  
### (Task 1: CRUD Operations + Task 2: Authentication System)

## 📌 Project Overview
This project is a User Management Web Application developed using Python Flask.
It is implemented in two phases as part of the Python Full Stack Web Development Internship.

- Task 1: Implemented full CRUD operations
- Task 2: Extended Task 1 by adding User Authentication (Register, Login, Logout)

The application demonstrates how frontend, backend, database, and authentication
work together in a real-world full-stack application.

---

## 🛠️ Technologies Used
- Backend: Python (Flask Framework)
- Frontend: HTML, CSS
- Database: SQLite
- Security: Werkzeug (Password Hashing)
- Tools: VS Code, GitHub, Web Browser

---

## 📁 Project Structure
python-fullstack-project/
│
├── app.py
├── init_db.py
├── database.db
├── README.md
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── edit.html
│
└── static/
    └── style.css

---

# ✅ TASK 1 – CRUD OPERATIONS

## 🔹 Task 1 Objective
To build a User Management System that allows:
- Add users
- View users
- Edit users
- Delete users
- Store data permanently using SQLite

## 🔄 Task 1 Flow
1. User submits form data
2. Flask receives request
3. Data stored in SQLite database
4. Records fetched and displayed in table
5. Edit/Delete updates database

---

# 🔐 TASK 2 – USER AUTHENTICATION SYSTEM

## 🔹 Task 2 Objective
To enhance Task 1 by implementing secure authentication so that only logged-in users
can access the dashboard and perform CRUD operations.

## ✨ Task 2 Features
- User Registration
- User Login
- Password Hashing
- Session Management
- Protected Dashboard
- Logout

---

## 🗄️ Database Design

### auth_users Table
- id (Primary Key)
- username (Unique)
- password (Hashed)

### users Table
- id
- name
- email

---

## 🔐 Authentication Flow

### Registration
1. User enters username and password
2. Password is hashed
3. Data stored securely
4. Redirect to login

### Login
1. User enters credentials
2. Password hash is verified
3. Session is created
4. User redirected to dashboard

### Session Management
- Session checked before accessing dashboard
- Unauthorized users redirected to login

### Logout
- Session cleared
- User redirected to login page

---

## ▶️ How to Run the Project
1. Install dependencies:
   pip install flask werkzeug
2. Initialize database:
   python init_db.py
3. Run the app:
   python app.py
4. Open browser:
   http://127.0.0.1:5000/register

---

## 📸 Screenshots
- Registration Page
- Login Page
- Dashboard
- Edit User
- Delete User

---

## 🎯 Learning Outcomes
- Full stack web development
- CRUD operations
- Secure authentication
- Session handling
- Real-world Flask application structure

---

## 🎤 Viva Explanation
This project implements a User Management System using Flask.
Task 1 covers CRUD operations, and Task 2 extends it with authentication
using password hashing and session management.
