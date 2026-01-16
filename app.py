from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


# ---------- Database Connection ----------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Home / Add / Search ----------
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    search = request.args.get('search')

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        if name and email:
            conn.execute(
                'INSERT INTO users (name, email) VALUES (?, ?)',
                (name, email)
            )
            conn.commit()
            flash('User added successfully!', 'success')
        conn.close()
        return redirect('/')

    if search:
        users = conn.execute(
            "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?",
            (f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        users = conn.execute('SELECT * FROM users').fetchall()

    conn.close()
    return render_template('index.html', users=users)


# ---------- Delete ----------
@app.route('/delete/<int:id>')
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('User deleted successfully!', 'danger')
    return redirect('/')


# ---------- Edit ----------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        conn.execute(
            'UPDATE users SET name = ?, email = ? WHERE id = ?',
            (name, email, id)
        )
        conn.commit()
        conn.close()
        flash('User updated successfully!', 'info')
        return redirect('/')

    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (id,)
    ).fetchone()
    conn.close()

    return render_template('edit.html', user=user)


# ---------- Run ----------
if __name__ == '__main__':
    app.run(debug=True)
