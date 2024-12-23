from flask import Flask

app=Flask(__name__)

@app.route("/")
def div():
    return "hello world"

if __name__=="main":
    app.run(debug=True)
