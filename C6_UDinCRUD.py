import os
from flask import Flask
import gunicorn
from flask_mongoengine import MongoEngine
import datetime
from flask import Flask, render_template, redirect, url_for, request, flash, session

from dotenv import load_dotenv
from pathlib import Path
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Flask-MongoEngine settings
MONGO_URI_BOOKODM = os.environ.get("MONGO_URI_BOOKODM")
app.config["MONGODB_SETTINGS"] = {
    'host': MONGO_URI_BOOKODM
}
db = MongoEngine(app)


class Book(db.Document):
    title = db.StringField(default="", maxlength=250)
    author = db.StringField(default="", maxlength=250)
    year = db.IntField(maxlength=4)
    ISBN = db.IntField(maxlength=13)
    short_description = db.StringField(default="", maxlength=2000)
    user = db.StringField(required=True, default="BookODM")
    creation_date = db.DateTimeField(default=datetime.datetime.now)
    comments = db.StringField(default="", maxlength=3500)
    rating = db.IntField(choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    genre = db.StringField(default="")
    private_view = db.StringField(default="off")
    book_thumbnail = db.StringField(default="")

    meta = {
        "auto_create_index": True,
        "index_background": True,
        "indexes": ["title"],
        "ordering": ["title"]
    }


@app.route("/")
@app.route("/index")
@app.route("/index.html")
def home_page():
    """
    The "R" in CRUD, a virtual library or stack of books to browse.
    """
    books_pagination = Book.objects()
    print(books_pagination.count())
    return render_template("index.html", books_pagination=books_pagination)


@app.route("/add_book")
def add_book():
    """
    Preparing for the "C" in CRUD, filling in the add book form.
    """
    return render_template("add_book.html")


@app.route("/save_book", methods=["POST"])
def save_book():
    """
    The "C" in CRUD, save the filled in add book form.
    """
    book = Book(
        title=request.form.get("title"),
        author=request.form.get("author"),
        year=request.form.get("year"),
        ISBN=request.form.get("isbn"),
        short_description=request.form.get("short_description"),
        comments=request.form.get("comments"),
        rating=request.form.get("rating"),
        genre=request.form.get("genre"),
        private_view=request.form.get("private_view")
    )

    try:
        book.save()
        flash("The book was saved!", "success")
    except Exception:
        flash("The book was NOT saved!", "danger")
    return redirect(url_for("home_page"))


@app.route("/edit_book/<book_id>")
def edit_book(book_id):
    """
    Preparing for the "U" in CRUD, updating the book form fields.
    """
    book = Book.objects.get(id=book_id)
    return render_template("edit_book.html", book=book)


@app.route("/update_book/<book_id>", methods=["POST"])
def update_book(book_id):
    """
    The "U" in CRUD, saving the changes made to the update book form fields.
    """
    book = Book.objects.get(id=book_id)
    fields = {
        "title": request.form.get("title"),
        "author": request.form.get("author"),
        "year": request.form.get("year"),
        "ISBN": request.form.get("isbn"),
        "short_description": request.form.get("short_description"),
        "comments": request.form.get("comments"),
        "rating": request.form.get("rating"),
        "genre": request.form.get("genre"),
        "private_view": request.form.get("private_view")
    }

    if fields["private_view"] != "on":
        fields["private_view"] = "off"

    try:
        book.update(**fields)
        flash("The book is updated!", "success")
    except Exception:
        flash("The book was NOT updated!", "danger")
    return redirect(url_for("home_page"))


@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    """
    The "D" in CRUD, deleting the book based on 'id'.
    """
    book = Book.objects.get(id=book_id)

    try:
        book.delete()
        flash("The book is deleted!", "success")
    except ReferenceError:
        pass
    except Exception:
        flash("The book was NOT deleted!", "danger")

    return redirect(url_for("home_page"))


if __name__ == "__main__":
    if os.environ.get("APPDEBUG") == "ON":
        app.run(host=os.environ.get("IP"),
                port=os.environ.get("PORT"), debug=True)
    else:
        app.run(host=os.environ.get("IP"),
                port=os.environ.get("PORT"), debug=False)
