import csv
import requests
import json
import pickle
import time

from urllib.parse import urlparse, unquote
from io import BytesIO    
from flask import Flask, session, render_template, render_template_string, send_file, request, redirect, url_for, abort
from flask_session import Session
from sqlalchemy import create_engine, Table, Integer, String, Boolean, Column, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

db_url = "mysql://root@db/books?"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(db_url)
db = scoped_session(sessionmaker(bind=engine))

@app.errorhandler(404)
def handle404(e):
    template = '''{{% extends "main-layout.html" %}}
{{% block body %}}
<h4 class="alert alert-danger my-3 w-40 text-center mx-auto">The Page {0} does not exist</h4>
{{% endblock %}}
'''.format(unquote(urlparse(request.url).path)[1:])
    return render_template_string(template), 404

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if session.get("user_name") is None:
            return render_template("login.html")
        elif session.get("admin") == True:
            return redirect(url_for("admin"))
        else:    
            return redirect(url_for("welcome"))
            

    if request.method == "POST":
        name = request.form.get("user_name")
        pwd = request.form.get("user_pwd")
        user = db.execute(f"SELECT * FROM users WHERE name = '{name}' AND password = '{pwd}'").fetchone()

        if user is None:
            return render_template("login.html", error_message="Invalid username or password")
        else:
            session["user_name"] = user.name
            if user.admin: 
                session["admin"] = True
                return redirect(url_for("admin"))
            else: 
                session["admin"] = False
                return redirect(url_for("welcome"))


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        name = request.form.get("user_name")
        pwd = request.form.get("user_pwd")

        if db.execute("SELECT count(id) from users").scalar() == 0:
            admin = True
            message = "Admin registration successful"
        else:
            admin = False
            message = "Registration successful"

        if db.execute(f"SELECT * FROM users WHERE name = '{name}'").rowcount == 1:
            return render_template("register.html", error_message="Username is already exists")
        else:
            db.execute(f"INSERT INTO users (name, password, admin) VALUES ('{name}', '{pwd}', {admin})")
            db.commit()
            return render_template("login.html", message=message)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if session.get("user_name") is None or session.get("admin") == False:
        return redirect("index")
    elif request.method == "POST":
        text = request.form.get("text")
        results = db.execute(
            f"SELECT * FROM books WHERE title LIKE '%{text}%' OR author LIKE '%{text}%' OR year LIKE '%{text}%' OR isbn LIKE '%{text}%' LIMIT 10").fetchall()
        return render_template("admin.html", user_name=session["user_name"], results=results, input_value=text, alert_message="No matches found, upload your own")
    else:
        return render_template("admin.html", user_name=session["user_name"])

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if session.get("user_name") is None:
        return redirect("index")
    elif request.method == "POST":
        text = request.form.get("text")
        results = db.execute(
            f"SELECT * FROM books WHERE title LIKE '%{text}%' OR author LIKE '%{text}%' OR year LIKE '%{text}%' OR isbn LIKE '%{text}%' LIMIT 10").fetchall()
        return render_template("welcome.html", user_name=session["user_name"], results=results, input_value=text, alert_message="No matches found")
    else:
        return render_template("welcome.html", user_name=session["user_name"])


@app.route("/logout")
def logout():
    session["user_name"] = None
    return redirect(url_for("index"))

@app.route("/backup/<string:isbn>", methods=["GET", "POST"])
def backup(isbn):
    book_info = db.execute(
        f"SELECT * FROM books WHERE isbn = '{isbn}'").fetchone()

    if request.method == "GET":
        if session.get("user_name") is None:
            return redirect("index")
        else:
            buffer = BytesIO()
            buffer.write(pickle.dumps([book_info,]))
            buffer.seek(0)
            return send_file(buffer, attachment_filename=isbn+".bkp", as_attachment=True)

    elif request.method == "POST":
        uf = request.files['file'].read()
        if len(uf) == 0:
            return render_template("admin.html", book=book_info, user_name=session["user_name"], reviews=reviews, alert_message="Invalid file")
        
        ds = pickle.loads(uf)

        try:
            db.execute(f"INSERT INTO books (isbn, title, author, year) VALUES ('{isbn}', '{ds[0].title}', '{ds[0].author}', {ds[0].year})")
            db.commit()

            return render_template("admin.html", user_name=session["user_name"], alert_message="File uploaded")
        except:
            return render_template("admin.html", user_name=session["user_name"], alert_message="Corrupted file")


@app.route("/books/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    reviews = db.execute(
        f"SELECT * FROM reviews WHERE isbn = '{isbn}'").fetchall()
    book_info = db.execute(
        f"SELECT * FROM books WHERE isbn = '{isbn}'").fetchone()
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "hmmbg2GLH2bzdmJ49tzFDA", "isbns": isbn}).json()
    res = res["books"][0]

    if request.method == "GET":
        if session.get("user_name") is None:
            return redirect("index")
        else:
            return render_template("book.html", book=book_info, user_name=session["user_name"], reviews=reviews, res=res)

    elif request.method == "POST":
        if db.execute(f"SELECT * FROM reviews WHERE username = '{session['''user_name''']}' AND isbn = '{isbn}'").rowcount > 0:
            return render_template("book.html", book=book_info, user_name=session["user_name"], alert_message="You've already done review", reviews=reviews, res=res)
        else:
            rating = request.form.get("rating")
            text = request.form.get("text")
            db.execute(f"INSERT INTO reviews(rating, text, isbn, username) VALUES ({rating}, '{text}', '{isbn}', '{session['''user_name''']}')")
            db.commit()
            reviews = db.execute(
                f"SELECT * FROM reviews WHERE isbn = '{isbn}'").fetchall()

            return render_template("book.html", book=book_info, user_name=session["user_name"], reviews=reviews, res=res)


@app.route('/api/<string:isbn>')
def api(isbn):
    book_info = db.execute(
        "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book_info is None:
        return abort(404)
    else:
        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": "hmmbg2GLH2bzdmJ49tzFDA", "isbns": isbn}).json()
        res = res["books"][0]
        review_count = res["work_ratings_count"]
        avg_score = res["average_rating"]
        result = {
            "title": book_info.title,
            "author": book_info.author,
            "year": book_info.year,
            "isbn": book_info.isbn,
            "review_count": review_count,
            "average_score": avg_score
        }
        return json.dumps(result)

if __name__ == "__main__":
    engine = create_engine(db_url)
    print(f"Waiting for {db_url} to be ready")
    while True:
        try:
            engine.raw_connection()
            break
        except Exception:
            print(".", end="", flush=True)
            time.sleep(1)


    db = scoped_session(sessionmaker(bind=engine))

    try:
        users = Table('users', MetaData(), Column('id',Integer,primary_key=True), Column('name',String(100)), Column('password',String(100)), Column('admin', Boolean, default=False))
        users.create(engine)
        db.commit()
    except:
        pass

    try:
        reviews = Table('reviews', MetaData(), Column('id',Integer,primary_key=True), Column('rating',Integer), Column('isbn',String(20)), Column('username',String(100)), Column('text',String(255)))
        reviews.create(engine)
        db.commit()
    except:
        pass

    try:
        book = Table('books', MetaData(), Column('id',Integer,primary_key=True), Column('isbn',String(20)), Column('title',String(255)), Column('author',String(100)), Column('year',Integer))
        book.create(engine)
        db.commit()

        f = open("books.csv")
        reader = csv.reader(f)

        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Added book {title}, {author}, {year} with ISBN = {isbn}")
        db.commit()

    except:
        pass
