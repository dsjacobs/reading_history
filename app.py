from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    db = get_db()
    cur = db.execute('SELECT id, title, author FROM books')
    users = cur.fetchall()
    return render_template('books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
