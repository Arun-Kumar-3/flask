from sqlalchemy import create_engine , MetaData , Table ,Column , Integer ,String ,insert ,inspect ,select
from flask import jsonify
meta=MetaData()
engine=create_engine('sqlite:///students.db' , echo = True)

students=Table(
    'students' , meta ,
    Column("id" , Integer , primary_key = True),
    Column("name" , String ),
    Column("age" , Integer)
)

meta.create_all(engine)


data=[
    {"id" : 1 , "name" : "1arun" , "age" : 11},
    {"id" : 2 , "name" : "2arun" , "age" : 21},
    {"id" : 3 , "name" : "3arun" , "age" : 31},
    {"id" : 4 , "name" : "4arun" , "age" : 41},
]

con=engine.connect()
#for user in data:
 #   new_user=insert(students).values(id = user["id"] , name=user["name"] , age=user["age"])
    
 #   print(new_user.compile().params)
 #   comit=con.execute(new_user)
 #   con.commit()


fetch_Data=students.select()
result_1=con.execute(fetch_Data)



#for row in result_1:
    
 #   print("hi  ",row)

print("this is last",students.c.keys())