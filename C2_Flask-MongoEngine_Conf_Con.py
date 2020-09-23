import os
from flask import Flask
import gunicorn
from flask_mongoengine import MongoEngine

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
