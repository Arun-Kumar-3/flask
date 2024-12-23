from flask import Flask , jsonify , request
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

meta=MetaData()
Base=declarative_base()

engine=create_engine("sqlite:///memeory.db" , echo=True)
app=Flask(__name__)
Session=sessionmaker(bind=engine)
session=Session()



class Loan(Base):
    __tablename__ = "loan" 
    id=Column(Integer , primary_key=True ,autoincrement=True)
    loan_amount = Column(Integer , nullable=False)
    user_relation=relationship("User", back_populates="loan_relation")
    bank_relation = relationship("Bank" , back_populates="loan_relation")

class User(Base):
    __tablename__ = "user"
     
    id = Column(Integer , primary_key=True , autoincrement=True)
    name = Column(String(100) , nullable=False)
    city = Column(String(30) , nullable=False)
            
    loan_id = Column(ForeignKey("loan.id"))

    loan_relation = relationship("Loan" , back_populates="user_realtion")

class Bank(Base):
    __tablename__ = "bank" 
    id= Column(Integer , primary_key=True ,autoincrement=True)
    bank_name = Column(String(30) , nullable=False)

    loan_id = Column(ForeignKey("loan.id"))

    loan_relation = relationship("Loan" , back_populates="bankt_relation")


Base.metadata.create_all(bind=engine)

table_mapping = {
    "loan": Loan,
    "user": User,
    "bank": Bank
}

@app.route("/items/<string:table_name>" , methods=['POST'])
def add_data(table_name):
    table_class = table_mapping.get(table_name)
    if not table_class:
        return "invalid table name"
    
    data=request.get_json()
    
    try:
        
        new_data=table_class.__table__.insert().values(data)
        with engine.connect() as con:
            con.execute(new_data)
            con.commit()
        return jsonify({"message" : "data added succesfully"})
    except Exception as e:
        return jsonify({"error"  : str(e) } )    


@app.route("/items/<string:table_name>",methods=["GET"])
def get_all_data(table_name):
    users=session.query(Loan).all()
    result=[row for row in users]
    return result

    

if __name__ == "__main__":
    app.run(debug=True)