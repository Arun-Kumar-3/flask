from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
SECRET_KEY = "secretkey"


def verify_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            token = auth_header.split(" ")[1]  # Extract token after "Bearer"
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        # Pass decoded payload to the route
        request.payload = payload
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if auth and auth.password == "pass":  # Ensure `auth` exists before using it
        expired = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        payload = {
            "username": auth.username,
            "exp": expired
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token}), 200

    return jsonify({"error": "Invalid credentials!"}), 401


@app.route("/protected", methods=["GET"])
@verify_token
def protect():
    # Access the decoded token payload
    username = request.payload["username"]
    return jsonify({"message": f"Welcome, {username}! Protected route accessed."})


if __name__ == "__main__":
    app.run(debug=True)
