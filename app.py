from flask import Flask, render_template, request, redirect, g
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
DATABASE = 'database.db'

def get_db_connection():
    conn = psycopg2.connect(host=os.environ['db_host'],
                            database="postgres",
                            user=os.environ['db_user'],
                            password=os.environ['db_password'])
    return conn

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute('SELECT * FROM book_app.books;')
    books = curr.fetchall()
    curr.close()
    conn.close()
    return render_template('index.html',books=books)

@app.route('/add_book')
def add_book():
    return render_template("add_book.html")
    
@app.route('/add_book',methods=['POST', 'GET'])
def add_book():
    if request.method == 'POST':
        result = request.form
        return render_template("result.html", result=result)
    # reader_name = request.form['Reader Name']
    # title = request.form['Title']
    # author = request.form['Author']
    # db = get_db()
    # db.execute('INSERT INTO books (reader_id, title, author) VALUES (?, ?)', (reader_name,title, author))
    # db.commit()
    # return redirect('/users')

@app.route('/books')
def books():
    return render_template("books.html")

@app.route('/setcookie', methods = ['POST', 'GET']) 
def setcookie(): 
    if request.method == 'POST': 
        user = request.form['nm'] 
        resp = make_response(render_template('cookie.html')) 
        resp.set_cookie('userID', user) 
        return resp 

@app.route('/getcookie') 
def getcookie(): 
    name = request.cookies.get('userID') 
    return '<h1>welcome '+name+'</h1>'
if __name__ == "__main__":
    app.run()

# @app.route('/books')
# def books():
#     db = get_db()
#     cur = db.execute('SELECT reader_name, title, author FROM books')
#     books = cur.fetchall()
#     return render_template('books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)