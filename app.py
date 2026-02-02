from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "super-secret-key"


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- AUTH ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        db = get_db()
        try:
            db.execute(
                "INSERT INTO auth_users (username, password) VALUES (?, ?)",
                (username, password),
            )
            db.commit()
            flash("Registration successful. Please login.", "success")
            return redirect("/login")
        except:
            flash("Username already exists!", "danger")

    return render_template("register.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM auth_users WHERE username=?", (username,)
        ).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user"] = username
            return redirect("/dashboard")

        flash("Invalid login credentials", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------- DASHBOARD / CRUD ----------
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    db = get_db()

    if request.method == "POST":
        db.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (request.form["name"], request.form["email"]),
        )
        db.commit()
        flash("User added successfully", "success")

    users = db.execute("SELECT * FROM users").fetchall()
    return render_template("dashboard.html", users=users)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "user" not in session:
        return redirect("/login")

    db = get_db()

    if request.method == "POST":
        db.execute(
            "UPDATE users SET name=?, email=? WHERE id=?",
            (request.form["name"], request.form["email"], id),
        )
        db.commit()
        flash("User updated", "info")
        return redirect("/dashboard")

    user = db.execute("SELECT * FROM users WHERE id=?", (id,)).fetchone()
    return render_template("edit.html", user=user)


@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect("/login")

    db = get_db()
    db.execute("DELETE FROM users WHERE id=?", (id,))
    db.commit()
    flash("User deleted", "danger")
    return redirect("/dashboard")


if __name__ == "__main__":
    app.run(debug=True)
