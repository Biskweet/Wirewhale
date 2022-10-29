from flask import Flask, render_template

from src import utils

app = Flask(__name__)

app.route("/", methods=["GET"])
def root():
    if utils.frames:
        return render_template("interface.html", utils.frames)

    return "You must run the parser first."
