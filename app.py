from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('todo.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS todos
                        (id INTEGER PRIMARY KEY, task TEXT NOT NULL, done BOOLEAN NOT NULL)''')
    conn.close()

@app.route('/')
def index():
    with sqlite3.connect('todo.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos")
        todos = cursor.fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    with sqlite3.connect('todo.db') as conn:
        conn.execute("INSERT INTO todos (task, done) VALUES (?, ?)", (task, False))
    return redirect(url_for('index'))

@app.route('/done/<int:todo_id>')
def done(todo_id):
    with sqlite3.connect('todo.db') as conn:
        conn.execute("UPDATE todos SET done = ? WHERE id = ?", (True, todo_id))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
