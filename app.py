from flask import Flask , render_template , url_for

app=Flask(__name__)

@app.route("/index")
def home():
    return render_template("about.html")

@app.route("/about/<name>")
def about(name):
    return render_template("index.html",name=name)

@app.route("/extend")
def extend():
    return render_template("extend.html")


@app.route("/profile/<username>")
def profile(username):
    return render_template("profile.html",username=username)

@app.route("/home1")
def home1():
    return render_template("home1.html")

@app.route("/about1")
def about1():
    return render_template("about1.html")



@app.route("/contact1")
def contact1():
    return render_template("contact1.html")

if __name__=="__main__":
    app.run(debug=True)