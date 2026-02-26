from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = "secret123"


# ================= DATABASE =================
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ================= DECORATORS =================

# ---- LOGIN REQUIRED ----
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if 'user' not in session:
            return redirect('/login')

        return f(*args, **kwargs)

    return wrapper


# ---- ADMIN REQUIRED ----
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if 'role' not in session:
            return redirect('/login')

        if session['role'] != "admin":
            return "❌ Access Denied (Admin Only)"

        return f(*args, **kwargs)

    return wrapper


# ================= HOME =================
@app.route('/')
def home():
    return redirect('/login')


# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']   # ✅ role added

        db = get_db()

        db.execute(
            "INSERT INTO users(username,password,role) VALUES(?,?,?)",
            (username, password, role)
        )
        db.commit()

        return redirect('/login')

    return render_template('register.html')


# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        db = get_db()

        user = db.execute(
            "SELECT * FROM users WHERE username=?",
            (request.form['username'],)
        ).fetchone()

        if user and check_password_hash(
                user['password'],
                request.form['password']):

            session['user'] = user['username']
            session['role'] = user['role']

            return redirect('/dashboard')

    return render_template('login.html')


# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ================= DASHBOARD =================
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# ================= ADMIN PANEL =================
@app.route('/admin')
@admin_required
def admin():

    db = get_db()
    users = db.execute(
        "SELECT username,role FROM users"
    ).fetchall()

    return render_template('admin.html', users=users)


# ================= STUDENTS =================
@app.route('/students')
@login_required
def students():

    db = get_db()

    students = db.execute(
        "SELECT * FROM students"
    ).fetchall()

    return render_template(
        'students.html',
        students=students
    )

# ================= ADD STUDENT =================
@app.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():

    if request.method == 'POST':

        db = get_db()

        db.execute(
            "INSERT INTO students(name,email,course) VALUES(?,?,?)",
            (
                request.form['name'],
                request.form['email'],
                request.form['course']
            )
        )
        db.commit()

        return redirect('/students')

    return render_template('add_student.html')


# ================= EDIT STUDENT =================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):

    db = get_db()

    student = db.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == 'POST':

        db.execute("""
            UPDATE students
            SET name=?, email=?, course=?
            WHERE id=?
        """,
        (
            request.form['name'],
            request.form['email'],
            request.form['course'],
            id
        ))
        db.commit()

        return redirect('/students')

    return render_template('edit_student.html', student=student)


# ================= DELETE (ADMIN ONLY) =================
@app.route('/delete/<int:id>')
@admin_required
def delete_student(id):

    db = get_db()
    db.execute("DELETE FROM students WHERE id=?", (id,))
    db.commit()

    return redirect('/students')


# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)