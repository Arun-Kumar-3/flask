from flask import Flask, request, jsonify
from flask_restful import Api ,Resource

app = Flask(__name__)
api=Api(app)
class APP(Resource):
    @app.route("/data", methods=["POST"])
    def receive_data():
        # 1. Parse the incoming JSON data from the request body
        data = request.get_json()  # request.get_json() gets the JSON data from request
        
        # 2. Print the received data (for debugging)
        print(data)  # This will print the JSON data that was sent to the server
        
        # 3. Send a JSON response back to the client
        return jsonify({"message": "Data received successfully!", "data": data}), 200

api.add_resource(APP,"/data/<")

if __name__ == "__main__":
    app.run(debug=True)
