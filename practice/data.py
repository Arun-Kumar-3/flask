from flask import Flask ,jsonify
from flask_restful import Api , Resource , abort , reqparse

app=Flask(__name__)
api=Api(app)

data={}

data_parser=reqparse.RequestParser()
data_parser.add_argument("name" , type=str , help="this is id's name ",required= True)
data_parser.add_argument("age" , type=int , help="this is id's age ",required= True)
data_parser.add_argument("city" , type=str , help="this is id's city ",required= True)


def already_in_data(data_id):
    if data_id in data:
        abort(402,message="id already in data")

def not_in_data(data_id):
    if data_id not in data:
        abort(404,message="id not found")

class Task(Resource):
    def get(self,data_id):
        not_in_data(data_id)
        return data[data_id]
    
    def post(self,data_id):
        return data[data_id]
    
    def put(self,data_id):
        already_in_data(data_id)
        args=data_parser.parse_args()
        data[data_id]=args
        return jsonify(data[data_id],400)
    
    def delete(self,data_id):
        not_in_data(data_id)
        del data[data_id]
        return jsonify("this data has been deleted :  ",202)
    
api.add_resource(Task,"/data/<int:data_id>")



if __name__=="__main__":
    app.run(debug=True)