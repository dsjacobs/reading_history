from flask import Flask, render_template, request, redirect, g
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

@app.route('/add_book', methods=['POST'])
def add_book():
    reader_name = request.form['Reader Name']
    title = request.form['Title']
    author = request.form['Author']
    db = get_db()
    db.execute('INSERT INTO books (reader_id, title, author) VALUES (?, ?)', (reader_name,title, author))
    db.commit()
    return redirect('/users')


@app.route('/books')
def books():
    db = get_db()
    cur = db.execute('SELECT reader_name, title, author FROM books')
    books = cur.fetchall()
    return render_template('books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)