from flask import Flask , jsonify , request
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
meta=MetaData()
app=Flask(__name__)
Base=declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer , primary_key=True  , autoincrement=True)
    name = Column(String , nullable=True)
    age =Column(Integer , nullable=True)
    loan_relation = relationship("Loan" , back_populates="user_relation")

    def __repr__(self):
        return f"User(id = {self.id}, name = {self.name} , age = {self.age})"

class Loan(Base):
    __tablename__ = "loan"
    id=Column(Integer , primary_key=True , autoincrement=True)
    amount = Column(Integer , nullable=True)
    user_id = Column(Integer , ForeignKey("user.id") )
    bank_id = Column(Integer , ForeignKey("bank.id") )
    user_relation = relationship("User" , back_populates="loan_relation")
    bank_relation  = relationship("Bank" , back_populates="bank_loan_relation")

    def __repr__(self):
        return f"Loan(id = {self.id} ,  amount = {self.amount} ,)"

class Bank(Base):
    __tablename__ = "bank"
    id = Column(Integer , primary_key=True)
    bank_name= Column(String(100) , nullable=True)
    bank_loan_relation = relationship("Loan" , back_populates="bank_relation")

    def __repr__(self):
        return f"Bank(id ={self.id} , bank_name = {self.bank_name})"

engine =create_engine("sqlite:///db.db" , echo=True)
session_factory= sessionmaker(bind = engine)
session =session_factory()
Base.metadata.create_all(engine)

# data=[
#     {"name" : "arun" , "age" : 21},
#     {"name"  : "kumar" , "age" : 33},
#     {"name" : "arun kumar" , "age" : 44}
# ]

tables={"user" : User,"loan" : Loan, "bank": Bank}

@app.route("/items/<string:table_name>",methods=["POST"])
def post(table_name):
    data=request.get_json()
    print(data)
    if table_name not in  tables:
        return "invalid table name"
    print("####################",table_name)
    if table_name == "user":
        
        
        new_user = User(name= data["name"] , age =data["age"] )
        session.add(new_user)
        session.commit()
        return jsonify({"message"  : "user added succesfully"})
    elif table_name=="loan":
        
        new_user = Loan(amount= data["amount"] , user_id= data["user_id"] , bank_id = data["bank_id"] )
        session.add(new_user)
        session.commit()
        return jsonify({"message"  : "user added succesfully"})
    elif table_name == "bank":
        
        new_user = Bank(bank_name= data["bank_name"] )
        session.add(new_user)
        session.commit()
        return jsonify({"message"  : "user added succesfully"})
    else:
        return jsonify({"message"  : "invalid table_name or field name"})
    
@app.route("/items/<string:table_name>",methods=["GET"])
def get_all_data(table_name):
    fields = request.args.get("fields", "*.*")
    t_name=tables.get(table_name)
    print("*************************",t_name)
    if table_name=="loan":
        
        
        users=[]
        # if table_name == "loan":
        all_users=session.query(t_name).join(User).join(Bank).all()
        for loan in all_users:
            users.append([{"loans" : {"id" : loan.id ,
                                    "amount" : loan.amount} },
                            { "user" :  {"id" : loan.user_relation.id ,
                                        "name" : loan.user_relation.name,
                                        "age" : loan.user_relation.age }},
                            {"bank" : {"bank_id" : loan.bank_relation.id,
                                    "bank_name" : loan.bank_relation.bank_name}}])
                
        return jsonify(users)
    all_data=session.query(t_name).all()
    print("******************",all_data)
    col_data=[]
    for row in all_data:
        col_data.append(row)
    return {"data" : col_data }






if __name__ =="__main__":
    app.run(debug=True)