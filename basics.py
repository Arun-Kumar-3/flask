from flask import Flask , url_for ,request

app=Flask(__name__)

@app.route("/")
def home():
    return f"this is home page "

@app.route("/about")
def about():
    return "this is about page"

@app.route("/user/<username>")
def user(username):
    return f"hi {username}"


@app.route("/product/<int:product_id>")
def product(product_id):
    return f"product id is : {product_id}"



@app.route("/submit",methods=["GET" ,"POST"])
def submit():
    if request.method=="POST":
        return "the form submited"
    return "submit the form"
           
@app.route("/search")
def search():
    query=request.args.get("query")
    return f"search query :{query}"

@app.route("/hello/<name>")
def hello(name):
    return f"hello , {name}"

@app.route("/calc/<int:num1>/<int:num2>")
def calc(num1,num2):
    return f" {num1 + num2} "

@app.route("/link")
def link():
    hello_url=url_for("hello",name="Arun")
    calc_url=url_for("calc",num1=13,num2=19)
    return f"the link is hello url : {hello_url} ,calc url : {calc_url}"

@app.route("/links")
def links():
    home_url=url_for("home")
    about_url=url_for("about")
    return f"home url : {home_url} , about_url : {about_url}"

if __name__=="main":
    app.run(debug=True)