import os
from flask import Flask
import gunicorn
from flask_mongoengine import MongoEngine
import datetime

from dotenv import load_dotenv
from pathlib import Path
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__, static_folder="static", template_folder="templates")

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
    user = db.StringField(required=True)
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
def hello():
    return ("This is a minimum viable Flask application, with a few extras. :-)")


if __name__ == "__main__":
    if os.environ.get("APPDEBUG") == "ON":
        app.run(host=os.environ.get("IP"),
                port=os.environ.get("PORT"), debug=True)
    else:
        app.run(host=os.environ.get("IP"),
                port=os.environ.get("PORT"), debug=False)
