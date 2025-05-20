import logging
logging.basicConfig(level=logging.DEBUG)

print("importing packages")
from flask import Flask, render_template, request, redirect, g
import os
import psycopg2

print("loading dotenv")
from dotenv import load_dotenv
load_dotenv()

print("starting app")
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
DATABASE = 'database.db'

print("db connection")
def get_db_connection():
    conn = psycopg2.connect(host=os.environ['db_host'],
                            database="postgres",
                            user=os.environ['db_user'],
                            password=os.environ['db_password'])
    return conn

print("define closed connection")
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

print("fetch from db on homepage")
@app.route('/')
def index():
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute('SELECT * FROM book_app.books;')
    books = curr.fetchall()
    curr.close()
    conn.close()
    return render_template('index.html',books=books)

# print("add book")
# def add_book():
#     result = request.form
#     return render_template("result.html", result=result)

print("books page")
@app.route('/books')
def books():
    return render_template("books.html")

print("set cookie")
@app.route('/setcookie', methods = ['POST', 'GET']) 
def setcookie(): 
    if request.method == 'POST': 
        user = request.form['nm'] 
        resp = make_response(render_template('cookie.html')) 
        resp.set_cookie('userID', user) 
        return resp 
    
print("get cookie")
@app.route('/getcookie') 
def getcookie(): 
    name = request.cookies.get('userID') 
    return '<h1>welcome '+name+'</h1>'
if __name__ == "__main__":
    app.run()

if __name__ == '__main__':
    app.run(debug=True)