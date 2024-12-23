from sqlalchemy  import *
from flask import Flask , jsonify
from flask_restful import  request , abort
from sqlalchemy.orm import *
meta=MetaData()


app=Flask(__name__)
engine=create_engine('sqlite:///mydb.db' , echo=True)

user=Table(
    "user" , meta ,
    Column("id" , Integer ,primary_key = True ,  autoincrement=True),
    Column("name" , String(50) , nullable=False),
    Column("age" , Integer  , nullable= False)
)

employee=Table(
    "employee" , meta ,
    Column("id" , Integer ,primary_key = True ,  autoincrement=True),
    Column("employee_name" , String(50) , nullable=False),
    Column("city" , String(50)  , nullable= False)
)
meta.create_all(engine)


@app.route("/get/<string:table_name>",methods=['GET'])
def get_all_records(table_name):
    with Connection(engine) as con:
        result = con.execute(text(f"select * from {table_name}"))
        jsonify()
            
@app.route("/post/<string:table_name>" , methods = ['POST'])
def post_data(table_name):
    data=request.get_json()
    if "name" and "age" in data:
        result=insert(table_name).values(name =data["name"] , age=data["age"])
        session.add(result)
        session.commit()
    if "employee_name" and "city" in data:
        result=insert(table_name).values(employee_name =data["employee_name"] , city=data["city"])
        session.add(result)
        session.commit()
    else:
        return "invalid data or invalid table name"
    
@app.route("/<string:table_name>/<int:id>",methods =['GET'])
def get_one(table_name , id):
    if table_name == "user":
        with Connection(engine) as con:
            result = con.execute(text(f"select * from {table_name} where id = {id}"))
            for row in result:
                return jsonify({'id' : row.id , 
                        'name' : row.name,
                        'age' : row.age})
                    
    elif table_name == "employee":
        with Connection(engine) as con:
            result = con.execute(text(f"select * from {table_name} where id = {id}"))
            for row in result:
                return jsonify({'id' : row.id , 
                        'employee_name': row.employee_name ,
                        'city' : row.city})
    else:
        return f"invalid table name or invalid data entered"
if __name__ == "__main__":
    app.run(debug=True)
