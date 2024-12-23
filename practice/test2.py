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
tabless=["user" , "loan" , "bank"]

@app.route("/items/<string:table_name>",methods=["POST"])
def post(table_name):
    data=request.get_json()
    print("**********************",data)
    print(data)
    t_name=tables.get(table_name)
    if  table_name not in tabless:
        return "invalid table name"
    print("####################",table_name)
    if table_name == "user" :
        
        
        new_user = User(name= data["name"] , age =data["age"] )
        session.add(new_user)
        session.commit()
        return jsonify({"data"  : {"id" :User.id ,
                                   "name" : User.name,
                                   "age" : User.age}},
                       {"message" : "user added succesfully"},
                       {"success" : True})
    elif table_name== "loan":
        
        new_user = Loan(amount= data["amount"] , user_id= data["user_id"] , bank_id = data["bank_id"] )
        session.add(new_user)
        session.commit()
        return jsonify({"data"  : {"id" : Loan.id ,
                                   "amount" : Loan.amount}},
                       {"message" : "user added succesfully"},
                       {"success" : True})
    elif table_name == "bank":
        
        new_user = Bank(id=data["id"],bank_name= data["bank_name"] )
        session.add(new_user)
        session.commit()
        return jsonify({"data"  : {"id" : Bank.id ,
                                   "bank_name" : Bank.bank_name}},
                       {"message" : "user added succesfully"},
                       {"success" : True})
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
                
        return jsonify({"data": users},
                       {"message" : "these are the all records in the table"},
                       {"success" : True})
    
    all_data=session.query(t_name).all()
    print("******************",all_data)
    col_data=[]
    if t_name == User:
        for row in all_data:
            col_data.append({"id" : row.id,
                             "name" : row.name,
                             "age" : row.age})
        return  jsonify({"data"  : col_data},
                       {"message" : "user get succesfully"},
                       {"success" : True})
    elif t_name == Bank:
        for row in all_data:
            col_data.append({"id" : row.id,
                             "bank_name" : row.bank_name})
        return  jsonify({"data"  : col_data},
                       {"message" : "user get succesfully"},
                       {"success" : True}) 
    else:
        return jsonify({"message" : "invalid table name"})

@app.route("/items/<string:table_name>/<int:id>" , methods=["GET"])
def get_id(table_name,id):
    t_name=tables.get(table_name)
    if t_name == User:
        user_data = session.query(User).get(id)
        if not user_data:
            return jsonify({"message" : "id is not available " })
        col_data={"id" : user_data.id,
                    "name" : user_data.name,
                    "age" : user_data.age}
        return jsonify({"data"  : col_data},
                       {"message" : "user get succesfully"},
                       {"success" : True})
    elif t_name == Bank:
        user_data = session.query(Bank).get(id)
        if not user_data:
            return jsonify({"message" : "id is not available " })
        col_data={"id" : user_data.id,
                    "bank_name" : user_data.bank_name,
                    }
        return jsonify({"data"  : col_data},
                       {"message" : "user get succesfully"},
                       {"success" : True})
    elif t_name==Loan:
            user_data = session.query(Loan).get(id)
            if not user_data:
                return jsonify({"message" : "id is not available " })
            col_data={"id" : user_data.id,
                    "amount" : user_data.amount,
                    
                    }
            return jsonify({"data"  : col_data},
                        {"message" : "user get succesfully"},
                       {"success" : True})




if __name__ =="__main__":
    app.run(debug=True)