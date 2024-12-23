from flask import Flask

app=Flask(__name__)

@app.route("/")
def first():
    return "welcome"
@app.route("/about")
def about():
    return "this is the about page"