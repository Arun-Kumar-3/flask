from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
SECRET_KEY = "secretkey"

roles = {
    "admin": {
        "role_name": "admin",
        "description": "An admin is a responsible manager, organizer, and decision-maker",
        "permissions": {
            "read": ["loan", "user", "bank", "product"],
            "write": ["loan", "user", "bank", "product"],
            "delete": ["loan", "user", "bank", "product"],
            "patch": ["loan", "user", "bank", "product"]
        }
    },
    "ch": {
        "role_name": "ch",
        "description": "CH is a leader, organizer, decision-maker, coordinator, and facilitator.",
        "permissions": {
            "read": ["loan", "user", "bank", "product"],
            "write": ["bank", "product"],
            "delete": ["product"],
            "patch": ["bank", "product"]
        }
    },
    "co": {
        "role_name": "co",
        "description": "CO is a collaborator, organizer, leader, communicator, and strategist.",
        "permissions": {
            "read": ["loan", "user", "bank", "product"],
            "write": ["loan", "user", "bank", "product"]
        }
    }
}

sign_up_user = {}

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    sign_up_user["mobile"] = data["mobile"]
    sign_up_user["role"] = data["role"]
    return jsonify({"message": "User added successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data["mobile"] == sign_up_user["mobile"]:
        expired = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        payload = {
            "role": sign_up_user["role"],
            "exp": expired
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Invalid mobile number"})

def valid_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}

def has_permission(role, table, operation):
    role_data = roles.get(role)
    print("******************",role_data)

    if not role_data:
        return False
    permissions = role_data.get("permissions", {})
    print("####################",permissions)

    operation_permissions = permissions.get(operation, [])
    print("*******************",operation_permissions)
    return table in operation_permissions

def permissions(operation):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({"message": "Authorization header is missing"})
            try:
                token = auth_header.split(" ")[1]
                payload = valid_token(token)
                if "error" in payload:
                    return jsonify(payload)
                role = payload.get("role")
                table = kwargs.get("table")
                if not has_permission(role, table, operation):
                    return jsonify({"message": "Access not granted"}),401
                return f(*args, **kwargs)
            except IndexError:
                return jsonify({"error": "Invalid authorization header format"})
        return wrapper
    return decorator

@app.route('/data/<table>', methods=['GET'])
@permissions("read")
def get_data(table):

    return jsonify({"message": f"Fetching data from table {table}"})

@app.route('/data/<table>', methods=['POST'])
@permissions("write")
def post_data(table):
    return jsonify({"message": f"Adding data to table {table}"})

@app.route('/data/<table>', methods=['PATCH'])
@permissions("patch")
def patch_data(table):
    return jsonify({"message": f"Patching data in table {table}"})

@app.route('/data/<table>', methods=['DELETE'])
@permissions("delete")
def delete_data(table):
    return jsonify({"message": f"Deleting data from table {table}"})

if __name__ == "__main__":
    app.run(debug=True)
