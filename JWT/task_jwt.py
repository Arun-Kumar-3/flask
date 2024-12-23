from flask import Flask , jsonify , request
import jwt
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from functools import wraps
import datetime

app=Flask(__name__)
SECRET_KEY = "secretkey"
roles ={
    "admin" : {
        "role_name"   : "admin" , 
        "discription" : "An admin is a responsible manager, organizer, and decision-maker",
        "permisions"  : {
                            "read" : ["loan" , "user" , "bank" , "product" ],
                            "write" : ["loan" , "user" , "bank" , "product" ],
                            "delete" : ["loan" , "user" , "bank" , "product" ],
                            "patch"   : ["loan" , "user" , "bank" , "product" ]
                }
    },
        
    "ch" :{ 
        "role_name"   : "ch" , 
        "discription" : "CH is a leader, organizer, decision-maker, coordinator, and facilitator.",
        "permisions"  : {
                            "read" : ["loan" , "user" , "bank" , "product"],
                            "write" : [ "bank" , "product" ],
                            "delete" : [ "product" ],
                            "patch"   : [ "bank" , "product" ]
                            }
    },

     "co" :{ 
        "role_name"   : "co" , 
        "discription" : "CO is a collaborator, organizer, leader, communicator, and strategist.",
        "permisions"  : {
                            "read" : ["loan" , "user" , "bank" , "product"],
                            "write" : [ "loan","user","bank" , "product" ],
                            
                            }
    },
    
    }
    

sign_up_user={}

@app.route("/signup" , methods=["POST"])
def signup():
    data=request.get_json()
    sign_up_user["mobile"] = data["mobile"]
    sign_up_user["role"] = data["role"]

    return jsonify({"message"  : "user added succesfully"})

@app.route("/login",methods=["POST"])
def login():
    data=request.get_json()
    if  data["mobile"]== sign_up_user["mobile"]:
        expired = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        payload={
            "role" : sign_up_user["role"],
            "exp" : expired

        }
        token =jwt.encode(payload,SECRET_KEY,algorithm="HS256")
        return jsonify({"token" : token})
    else:
        return jsonify({"message" : "invalid mobile number"})
    
def valid_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return jsonify({"error" : "token has expired"})
    except jwt.InvalidTokenError :
        return jsonify({"error" : "invalid token "})
    
def has_permision(role,table,oparation):
    role_name=roles.get(role,{})
    print("****************",role_name)

    role_name_perminsions=role_name.get(role_name,{})
    print("**************",role_name_perminsions)

    role_permision=role_name_perminsions.get("premisions")
    print("############################",role_permision)

    if oparation == "get":
        oparation_name = "read"
    elif oparation_name == "post":
        oparation_name = "write"
    elif oparation_name == "putch":
        oparation_name == "patch"
    elif oparation_name == "delete":
        oparation_name = "delete"
    tables=role_permision.get(oparation_name)
    print("**********************",tables)

    if table in tables:
        return oparation
    return False



    
def primisions(oparation):
    def decorator(f):
        def wrapper(*args,**kwargs):
            auth_header=request.headers.get('Authorization')
            if not auth_header :
                return jsonify({"message" : "authorization header is missing"})
            try:
                token = auth_header.split("")[1]
                payload=valid_token(token)
                if "error" in payload:
                    return jsonify(payload)
                role=payload.get("role")
                table=kwargs.get("table")
                if not has_permision(role,table,oparation):
                    return jsonify({"message" : "access forbiden"})
                return func(*args,**kwargs)
            except IndexError:
                return jsonify({"error" : "invalid authorization header format"})
        return wrapper
    return decorator


@app.route('/data/<table>', methods=['GET'])
@primisions("get")
def get_data(table):

    return jsonify({"message": f"Fetching data from table {table}"})

@app.route('/data/<table>', methods=['POST'])
@primisions("post")
def get_data(table):
    
    return jsonify({"message": f"Fetching data from table {table}"})

@app.route('/data/<table>', methods=['PATCH'])
@primisions("patch")
def get_data(table):
    
    return jsonify({"message": f"Fetching data from table {table}"})

@app.route('/data/<table>', methods=['DELETE'])
@primisions("delete")
def get_data(table):
    
    return jsonify({"message": f"Fetching data from table {table}"})




        

