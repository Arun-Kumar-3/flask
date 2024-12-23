from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper


app = Flask(__name__)
engine = create_engine("sqlite:///jwt.db")
Session_factory = sessionmaker(bind=engine)
session=Session_factory()

SECRET_KEY = "secretkey"

metadata=MetaData()

Base = declarative_base()
# print("*****************",Base)
metadata.reflect(bind=engine)

table_names= metadata.tables.keys()
print("********************",table_names)

class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer , primary_key=True , autoincrement=True)
    role_name = Column(String(100), nullable = False)
    discription = Column(String(500) , nullable=False)
    
    permition = Column(JSON)

    
    def __repr__(self):
        return f"Roles(id = {self.id} , role = {self.role} , role_name = {self.role_name} , discription = {self.discription} , permition = {self.permition})"

class Signup(Base):
    __tablename__ = "signup"
    
    mobile = Column(Integer ,nullable=False)
    role_id = Column(Integer , primary_key=True)

    

# roles = {
#     "admin": {
#         "role_name": "admin",
#         "description": "An admin is a responsible manager, organizer, and decision-maker",
#         "permissions": {
#             "read": ["loan", "user", "bank", "product"],
#             "write": ["loan", "user", "bank", "product"],
#             "delete": ["loan", "user", "bank", "product"],
#             "patch": ["loan", "user", "bank", "product"]
#         }
#     },
#     "ch": {
#         "role_name": "ch",
#         "description": "CH is a leader, organizer, decision-maker, coordinator, and facilitator.",
#         "permissions": {
#             "read": ["loan", "user", "bank", "product"],
#             "write": ["bank", "product"],
#             "delete": ["product"],
#             "patch": ["bank", "product"]
#         }
#     },
#     "co": {
#         "role_name": "co",
#         "description": "CO is a collaborator, organizer, leader, communicator, and strategist.",
#         "permissions": {
#             "read": ["loan", "user", "bank", "product"],
#             "write": ["loan", "user", "bank", "product"]
#         }
#     }
# }

# sign_up_user = {}

class Loan(Base):
    __tablename__ = "loan"
    id = Column(Integer,primary_key=True , autoincrement=True)
    amount = Column(Integer , nullable=False)
    user_id = Column(Integer , ForeignKey("user.id"))
    bank_id = Column(Integer ,ForeignKey("bank.id"))

    user_relation = relationship("User" , back_populates="relate_to_loan")
    bank_relation = relationship("Bank" , back_populates="relate_to_bank")

class User(Base):
    __tablename__ = "user"
    id = Column(Integer , primary_key=True,autoincrement=True)
    name= Column(String(100) , nullable=False)
    age = Column(Integer , nullable=False)

    relate_to_loan = relationship("Loan" ,back_populates="user_relation")

class Bank(Base):
    __tablename__ = "bank"
    id = Column(Integer,primary_key=True)
    bank_name = Column(String(40) , nullable=False)

    relate_to_bank = relationship("Loan" , back_populates="bank_relation")

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer,primary_key=True,autoincrement=True)
    city = Column(String(100),nullable=False)

Base.metadata.create_all(engine)


@app.route("/roles",methods = ['POST'])
def add_role():
    data = request.get_json()
    # print("******************",data)
    try:
        json_c_data = data.get("permission")
        # print("*************",json_c_data)
        new_data = Roles(role_name = data["role_name"]  , discription = data["discription"],permition = json_c_data )
        session.add(new_data)
        session.commit()
        return jsonify({"message" : "role added succesfully" , "your_role_id"  : new_data.id})
    except Exception as e:
        return jsonify({"error" : str(e)})
    
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    new_data = Signup(role_id = data["role_id"] , mobile = data["mobile"])
    session.add(new_data)
    session.commit()
    return jsonify({"message": "User added successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    # print("^^^^^^^^^^^",data)
    mobile_record = session.query(Signup).filter(Signup.mobile == data["mobile"]).first()

    # print("$$$$$$$$$$$$$$$$$$$" , mobile_record)
    mobile = mobile_record.mobile
    # print("*********",mobile)
    if data["mobile"] == mobile:
        expired = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        record = session.query(Roles).filter(Roles.id == mobile_record.role_id).first()
        
        payload = {
            "role": record.role_name,
            # "permition" : record.permition,
            "exp": expired
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})
    else:
        return jsonify({"message": "Invalid mobile number"})

def valid_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}


def has_permission(role, table, operation ):
    try:
        # oparations = permition.get(operation,[])
        # print("************" , oparations)
        # return table in oparations

        record = session.query(Roles).filter_by(role_name = role).first()
        print("*********",record)
        premision = record.get("permition",{})
        print("###############",premision)
        permistion_oparation = premision.get(operation,[])
        return  table in permistion_oparation
    except Exception as e:
        return jsonify({"error " : str(e)})
    
    return False

 
def permissions(operation):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({"message": "Authorization header is missing"})
            try:
                token = auth_header.split(" ")[1]
                payload = valid_token(token)
                if "error" in payload:
                    return jsonify(payload)
                role = payload.get("role")
                # print("*********** : payload role : ",role)
                table = kwargs.get("table")
                # permition  =payload.get("permition",{})
                # print("################",permition)
                if not has_permission(role, table, operation ):
                    return jsonify({"message": "Access not granted"}),401
                return f(*args, **kwargs)
            except IndexError:
                return jsonify({"error": "Invalid authorization header format"})
        return wrapper
    return decorator

@app.route('/data/<table>', methods=['GET'])
@permissions("read")
def get_data(table):
    model_class = next(
            (mapper.class_ for mapper in Base.registry.mappers if mapper.persist_selectable.name == table),
            None,
        )
    print("******",model_class)
    try:
        total_record = session.query(model_class).all()

        all_record = []
        for colun in total_record:
            colun_dict=colun.__dict__.copy()
            colun_dict.pop('_sa_instance_state', None)
            all_record.append(colun_dict)

        return jsonify({"data" : all_record} , 
                       {"message" : "data get successfully"},
                       {"sucess" : True})
    except Exception as e:
        return jsonify({"error"  : str(e)})


@app.route('/data/<table>', methods=['POST'])
@permissions("write")
def post_data(table):
    model_class = next(
        (mapper.class_ for mapper in Base.registry.mappers if mapper.persist_selectable.name == table),None
    )
    data=request.get_json()
    t_name = metadata.tables[table]
    try:
        result = session.execute(t_name.insert().values(data))
        session.commit()
        columns =[column.name for column in model_class.__table__.columns]
        Datas={}
        for key,value in data.items():
            Datas[key] = value
        Datas["id"] = result.inserted_primary_key[0]
        
        return jsonify({"data" : Datas},
                    {"message": "data added succesfully"},
                    {"success" : True}
                    )
    except Exception as e:
        return jsonify({"error" : str(e)})

@app.route('/data/<table>/<int:id>', methods=['PATCH'])
@permissions("patch")
def patch_data(table,id):
    data =request.get_json()
    model_class = next((mapper.class_ for mapper in Base.registry.mappers if mapper.persist_selectable.name == table),None)
    print("*****************model class",model_class)
    user_Data = session.query(model_class).get(id)

    try:
        columns = [column.name for column in model_class.__table__.columns]
        print("*********** columns",columns)
        for key,values in data.items():
            if key in columns:
                setattr(user_Data , key , values)           
        session.commit()
        Data={}
        for k ,v in data.items():
            Data[k] = v
        

        return jsonify({"data" : Data},
                       {"message": "this is patch method"},
                       {"success" : True})
    except Exception as e:
        return jsonify({"error" : str(e)})
    

@app.route('/data/<table>/<int:id>', methods=['DELETE'])
@permissions("delete")
def delete_data(table,id):
    model_class = next(
        (mapper.class_ for mapper in Base.registry.mappers if mapper.persist_selectable.name == table),None
    )
    result = session.query(model_class).get(id)
    session.delete(result)
    session.commit()
    return jsonify({"message" : "Data deleted succesfully"})


    

@app.route("/roles", methods=['POST'])
def addd_role():
    data = request.get_json()
    print("******************", data)
    try:
        json_c_data = data.get("permission")
        print("*************", json_c_data)
        new_data = Roles(
            role_name=data["role_name"],
            discription=data["discription"],
            permition=json_c_data
        )
        session.add(new_data)
        session.commit()
        return jsonify({
            "message": "Role added successfully",
            "your_role_id": new_data.id  
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    
if __name__ == "__main__":
    app.run(debug=True)
