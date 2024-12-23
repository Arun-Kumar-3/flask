from flask import Flask , jsonify
from flask_restful import Api, Resource , abort , reqparse
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
api=Api(app)
#db=SQLAlchemy(app)

students={}

stud_stu_id=reqparse.RequestParser()
stud_stu_id.add_argument("name" , type=str , help="name of the student" , required=True)
stud_stu_id.add_argument("age" , type=int , help="age of the student" , required=True)
stud_stu_id.add_argument("city" , type=str , help="city of the student" , required=True)

def is_not_in_students(stu_id):
    if stu_id not in students:
        abort(404,message="student id not found ")
def is_in_students(stu_id):
    if stu_id in students:
        abort(message="id in students")

class Students(Resource):
    def get(self,stu_id):
        is_not_in_students(stu_id)
        return {"students" : students[stu_id] }
    
    def post(self,stu_id):
        return {"students" : students[stu_id] }
    
    def put(self,stu_id):
        is_in_students(stu_id)
        args=stud_stu_id.parse_args()
        students[stu_id]=args
        return {"students" : students[stu_id]}
    


    def delete(self,stu_id):
        is_not_in_students(stu_id)
        del students[stu_id]
        return {"students" : f" {stu_id} is deleted"}
    
api.add_resource(Students,"/students/<int:stu_id>")
    
if __name__=="__main__":
    app.run(debug=True)
