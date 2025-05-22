import logging
from logging import FileHandler,WARNING
logging.basicConfig(level=logging.DEBUG)

print("importing packages")
from flask import Flask, render_template,request, redirect, g, url_for
from flask_bootstrap import Bootstrap5
import os
import psycopg2
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

print("loading dotenv")
from dotenv import load_dotenv
load_dotenv()

print("starting app")
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.debug = True
DATABASE = 'database.db'
file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

print("form setup")
foo = "\S_4VQB&'ZU]eGk>"
app.secret_key = foo
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

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

class BookForm(FlaskForm):
    title = StringField('Title?', validators=[DataRequired(), Length(10, 40)])
    author= StringField('Author?', validators=[DataRequired(), Length(10, 40)])
    reader = StringField('Reader?', validators=[DataRequired(), Length(10, 40)])
    submit = SubmitField('Submit')

print("add book",methods = ['POST', 'GET'])
@app.route('/add_book')
def add_book():
    form = BookForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            title = form.title.data
            author = form.author.data
            reader = form.reader.data
    return render_template('add_book.html', form=form)

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