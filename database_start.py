import sqlite3
from flask import Flask, g, render_template, request

app = Flask(__name__)
DATABASE = 'database.db'

def connect_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = connect_db()
    db.execute('''
    CREATE TABLE IF NOT EXISTS users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
    )
    '''
    )
    db.commit()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/join', methods=['POST', 'GET'])
def join():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('''
        INSERT INTO users (username, password, email) VALUES (?, ?, ?)
        ''', (username, password, email))
        db.commit()
    return render_template("join.html")

@app.route('/partipicants')
def participants():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
    SELECT * FROM users
    ''')
    users = cursor.fetchall()
    return render_template("user.html", data=users)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)