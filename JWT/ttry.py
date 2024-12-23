from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


app = Flask(__name__)
engine = create_engine("sqlite:///example.db")
Session_factory = sessionmaker(bind=engine)
session=Session_factory()
Base = declarative_base()
metadata=MetaData()

class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer , primary_key=True , autoincrement=True)
    role_name = Column(String(100), nullable = False)
    discription = Column(String(500) , nullable=False)
    
    


Base.metadata.create_all(engine)


@app.route("/show_colums" , methods=["GET"])
def show():
    colums= [column.name for column in Roles.__table__.columns]
    print("******************",colums)
    all_data = session.execute(select(Roles).get(1))

    


    return jsonify({"message" : all_data})


@app.route("/post",methods= ["POST"])
def post():
    data = request.get_json()
    print("*********** data : " , data)
    colums= [column.name for column in Roles.__table__.columns]
    print("******************",colums)
    for i in colums:
        print("**********",i)
        # new_data = Roles(id = ,role_name = ,discription = )
    result= session.execute(insert(Roles).values(data))
    print("********",result)
    
    session.commit()
    return jsonify({"message" : "success"})

if __name__ =="__main__":
    app.run(debug=True)

