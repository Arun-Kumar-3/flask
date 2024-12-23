from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

# Create the Flask app and configure the database URI
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Users table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Check if user ID is not in the Users table
def is_not_in_Users(user_id):
    user = Users.query.get(user_id)
    if not user:
        abort(404, message="User ID not found")

# Check if user ID is in the Users table
def is_in_users(user_id):
    user = Users.query.get(user_id)
    if user:
        abort(400, message="User ID already exists")

# Route to add a new user (POST)
@app.route("/user", methods=['POST'])
def post_user():
    data = request.get_json()
    
    # Check if user already exists
   
    
    new_user = Users(name=data["name"], age=data["age"])
    db.session.add(new_user)
    db.session.commit()
    
    print(f"User ID: {new_user.id} added successfully")  # Printing the generated ID
    
    return jsonify({"message": "User added successfully"}), 200

# Route to get a user by ID (GET)
@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    
    user_data = {'id': user.id, 'name': user.name, 'age': user.age}
    return jsonify(user_data)

# Route to update user details (PUT)
@app.route("/user/<int:user_id>", methods=["PUT"])
def put_user(user_id):
    data = request.get_json()
    
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    
    user.name = data['name']
    user.age = data['age']
    db.session.commit()
    
    return jsonify({'message': 'Data updated successfully'}), 200

# Route to delete a user by ID (DELETE)
@app.route("/user/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'Data deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
