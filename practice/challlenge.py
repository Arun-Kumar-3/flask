from flask import Flask ,jsonify
from flask_restful import request , abort
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']   = 'sqlite:///new.db'
db=SQLAlchemy(app)

class Employees(db.Model):
    id =db.Column(db.Integer , primary_key=True , autoincrement=True)
    name = db.Column ( db.String(100) , nullable=False)
    age= db.Column(db.Integer  ,nullable = False)

with app.app_context():
    db.create_all()

@app.route("/employee" , methods=['POST'])
def employee():
    data=request.get_json()
    emp =Employees(name = data['name'] , age = data['age'])
    db.session.add(emp)
    db.session.commit()
    return jsonify({"message " : "new employee added succesfully"}),200

@app.route("/employee/<int:emp_id>", methods=['GET'])
def get_employee(emp_id):
    emp =Employees.query.get(emp_id)
    print(emp)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    if not emp or emp is None:
        return jsonify({"message" : "employee id not found"})
    emp_data={"name" : emp.name , "age" : emp.age}
    return jsonify(emp_data),200

@app.route("/employee/<int:emp_id>",methods=['PUT'])
def update_employeee(emp_id):
    data=request.get_json()
    emp =Employees.query.get(emp_id)
    if not emp:
        jsonify({"message" : "employee id not found"})
    emp.name = data['name']
    emp.age = data['age']
    db.session.commit()
    return jsonify({"message" : "updated succesfully"}),200

@app.route("/employee/<int:emp_id>" , methods=['PATCH'])
def patch_update(emp_id):
    data=request.get_json()
    emp =Employees.query.get(emp_id)
    if not emp:
        return jsonify({"message" : "employee id not found"})

    if 'name' in data:
        emp.name = data['name']
    if 'age' in data:
        emp.age = data['age']
    else:
        print("invalid data you enterd")
    db.session.commit()
    return jsonify({"message" : 'succesfullu patched'}),200

@app.route("/employee/<int:emp_id>" , methods=['DELETE'])
def delete_emp(emp_id):
    
    emp =Employees.query.get(emp_id)
    if not emp:
        return jsonify({"message" : "employee id not found"})
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"message" : "data has been deleted"})


@app.route('/employee',methods=['GET','POST' ,'OPTIONS'])
def options():
    if request.method=='OPTIONS':
        response=jsonify({"message" : "this oparations are available GET POST OPTIONS"})
        response.headers['Allow'] = 'GET , POST , OPTIONS'
        return response,200
    elif request.method==['GET']:
        return jsonify({"message" : "get method are allowed"}),200
    elif request.method==['POST']:
        return jsonify({"message" : "post methods are allowed"}),201
    else:
        return jsonify({"error" : response.status_code})
    
@app.route('/employee',methods=['GET' , 'HEAD'])
def head():
    if request.method == 'HEAD':
        response=jsonify()
        response.headers['Custum-Headers'] = 'this is the head request'
        return response,200
    elif request.method == 'GET':
        return jsonify({"message" : "GET method are accesed"}),200

if __name__ == '__main__':
    app.run(debug=True)
    