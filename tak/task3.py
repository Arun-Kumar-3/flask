from flask import Flask,jsonify,request
from sqlalchemy import *
from sqlalchemy.orm import *
meta=MetaData()

app=Flask(__name__)
engine=create_engine('sqlite:///loan.db')
Session=sessionmaker(bind=engine)
session=Session()



metadata = MetaData()
metadata.reflect(bind=engine)


user=Table(
    "user" , meta,
    Column("id" , Integer ,primary_key=True, autoincrement=True),
    Column("name" , String(100) , nullable=False),
    Column("city" , String(100) , nullable=False)
)

product= Table(
    "product" , meta, 
    Column("id" , Integer , primary_key=True ,autoincrement=True),
    Column("customer_name" , String(100) , nullable=False)
)

loan=Table(
     "loan" , meta,
    Column("id" , Integer , primary_key= True  , autoincrement=True),
    Column("loan_amount" , Integer , nullable=False),
    Column("user_id" , ForeignKey("user.id") ),
    Column("product_id" , ForeignKey("product.id"))

)

table_names={"user" : "user" , "product" : "product" , "loan" : "loan"}          
@app.route("/items/<string:table_name>", methods=['POST'])
def post(table_name):
    
    if table_name not in table_names:
        return "invalid table name"
    try:
        if table_name == "user":
            name = user
        elif table_name == "product":
            name == product
        elif table_name == "loan":
            name == loan
        print("********************************",name)
        data=request.get_json()
        new_data= insert(name).values(data)
        with Connection(engine) as con:
            dat=con.execute(new_data)
        
            session.add(dat)
            session.commit()
        return "new data added succesfully"
    except Exception as e:
        return jsonify({"error" : str(e)}),500
    
@app.route("/items/<string:table_name>" , methods=['GET'])
def get_table_data(table_name):
    if not table:
        return "invalid table name"
    with Connection(engine) as con:
        result = con.execute(select(table_name))
        all_data=[dict(row) for row in result]
        return jsonify(all_data)

@app.route("/items/<string:table_name>/fields:*.*")
def all_forign_key(table_name):
    if not table:
        return "invalid table name"
    with Connection(engine)  as con:
        result=con.execute(text("select l.id , l.loan_amount , l.user_id , u.id , u.name , u.city , p.id , p.customer_name from loan as l join user as u on loan.user_id =user.id  join product as p on user.id = product.id" )) 
                                
        
        all_data=[dict(row) for row in result]
        return jsonify(all_data)
    

if __name__=="__main__":
    app.run(debug=True)