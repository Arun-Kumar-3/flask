from flask import Flask , jsonify  , request
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *
meta=MetaData()
engine= create_engine("sqlite:///latest.db" , echo=True)
app=Flask(__name__)
Base=declarative_base()
Session=sessionmaker(bind=engine)
session=Session()


user =table(
Column("id",Integer , primary_key=True , autoincrement=True),
Column("name",String(50),nullable=False),
Column("age",Integer , nullable=False))

Base.metadata.create_all(engine)

@app.route("/items/<string:table_name>",methods=["POST"])
def add_new_user(table_name):
    data=request.get_json()
    # new_user = User(name = data["name"]  , age=data["age"])
    # session.add(new_user)
    # session.commit()

    add_user= user.name= data["name"] , user.age=data["age"]
    session.add(add_user)
    session.commit()
        

 
        
    return "user added succesfully"

if __name__ == "__main__":
    app.run(debug=True)