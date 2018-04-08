from flask import render_template
from application import app


@app.route("/", endpoint='index')
def hello():
    return render_template("index.html")
