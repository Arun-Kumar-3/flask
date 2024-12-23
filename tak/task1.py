from flask import Flask , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource , request
from collections import OrderedDict

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db=SQLAlchemy(app)


class Table1(db.Model):
    id=db.Column(db.Integer , primary_key=True , autoincrement=True)
    name=db.Column(db.String(100) , nullable=False)
    age=db.Column(db.Integer , nullable=False)

class Table2(db.Model):
    id=db.Column(db.Integer , primary_key = True , autoincrement=True)
    city=db.Column(db.String(100) ,nullable=False)
    join_month=db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/list_tables',methods=['GET'])
def get_list_tables():
    return jsonify({"data" : ["Table1" ,
                              "Table2"] , 
                    "message" : "these are the tables" , 
                    "success" : True}),200

@app.route("/table/<string:table_name>", methods=['GET'])
def get_field(table_name):
    if table_name == "Table1":
        users=Table1.query.all()
        if users is not None:
            user_data=[{"id" : user.id , "name" : user.name , "age" : user.age} for user in users ]
            return jsonify({"data" : [user_data] ,
                            "message" : "these are the all records" ,
                            "Success" : True}),200
        else:
            return jsonify({"message"  : "no records found"})
        
    elif table_name == "Table2":
            
            users=Table2.query.all()
            if users is not None:
               
                user_data=[{"id" : user.id , "city" : user.city , "join_month" : user.join_month} for user in users]
                return jsonify({"data" : [user_data] ,
                                "message" : "these are the all records" ,
                                "Success" : True}),200
            else:
                return jsonify({"message"  : "no records found"})
    else:
        return jsonify({"message" : "the table name has invalid"}),404

@app.route("/table/post/<string:table_name>",methods=['POST'])
def post(table_name):
    data=request.get_json()
    if table_name == "Table1":
        new_user=Table1(name=data['name'] , age=data['age'])
        
        db.session.add(new_user)
        db.session.commit()
        ordered=OrderedDict({"id" : new_user.id ,
                                "name" : new_user.name ,
                                "age" :  new_user.age})
        return jsonify({"data" : [ordered],
                        "message" : "these are the fields and values",
                        "success" : True}),201
    if table_name =="Table2":
        new_user=Table2(city=data['city'] , join_month=data['join_month'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"data" : [{"id" : new_user.id ,
                                    "city" : new_user.city ,
                                    "month" : new_user.join_month}],
                        "message" : "these are the fields",
                        "success" : True}),201
    else:
        return jsonify({"message" : "the table name was entered wrong"}),404
    
@app.route("/table/put/<string:table_name>/<int:user_id>" , methods=['PUT'])
def update(table_name,user_id):
    data=request.get_json()
    if table_name =="Table1":
        if "name" and "age" in data:
            user=Table1.query.get(user_id)
            if user is not None:
                user.name=data['name']
                user.age=data["age"]
                db.session.commit()
                return jsonify({"data" : [{"id" : user.id,
                                            "name" : user.name ,
                                             "age" :  user.age}],
                                "message" : "updated succesfully",
                                "success" : True}),202
            else:
                return jsonify({"message" : "the user id not found"}),404
        else:
            return jsonify({"message" : "there is no table name or field name invalid"}),404
    elif table_name =="Table2":        
        if "city" and "join_month" in data:
            user=Table2.query.get(user_id)
            if user is not None:
                user.city=data['city']
                user.join_month=data["join_month"]
                db.session.commit()
                return jsonify({"data" : [{"id" : user.id,
                                            "city" : user.city ,
                                             "join_month" :  user.join_month}],
                                "message" : "updated succesfully",
                                "success" : True}),202
            
            else:
                return jsonify({"message" : "the user id not found"}),404
        else:
            return jsonify({"message" : "there is no table name or field name invalid"}),404
    else:
        return jsonify({"message" : "there is no table name or field name invalid"}),404

@app.route("/table/patch/<string:table_name>/<int:user_id>" ,methods=['PATCH'])
def patch_update(table_name,user_id):
    data=request.get_json()
    if table_name =="Table1":
        if "name" or "age" in data:
            user=Table1.query.get(user_id)
            if user is not None:
                if "name" in data:
                    user.name=data['name']
                if "age" in data:
                    user.age=data["age"]
                else:
                    return jsonify({"message" : "invalid field"}),404
                db.session.commit()
                return jsonify({"data" : [{"id" : user.id,
                                            "name" : user.name ,
                                             "age" :  user.age}],
                                "message" : "updated succesfully",
                                "success" : True}),202
            else:
                return jsonify({"message" : "the user id not found"}),404
    elif table_name =="Table2":
        if "city" or "join_month" in data:
            user=Table2.query.get(user_id)

            if user is not None:
                if "city" in data:
                    user.city=data['city']
                if "join_month" in data:
                    user.join_month=data["join_month"]
                else:
                    return jsonify({"message" : "invalid field"}),404
                db.session.commit()
                return jsonify({"data" : [{"id" : user.id,
                                            "name" : user.name ,
                                             "age" :  user.age}],
                                "message" : "updated succesfully",
                                "success" : True}),202
            else:
                return jsonify({"message" : "the user id not found"}),404
    else:
        return jsonify({"message" : "there is no table name or field name invalid"}),404
        
@app.route("/table/delete/<string:table_name>/<int:user_id>" , methods=['DELETE'])
def delete(table_name,user_id):
    if table_name=="Table1":
        user=Table1.query.get(user_id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message" : "the data has been deleted"})
        else:
            return jsonify({"message" : "no id detected "})
    
    elif table_name=="Table2":
        user=Table2.query.get(user_id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message" : "the data has been deleted"})
        else:
            return jsonify({"message" : "no id detected "})
    else:
        return jsonify({"message" : "invalid table name"})
    
    

if __name__ == '__main__':
    app.run(debug=True)