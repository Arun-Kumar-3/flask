from typing import *
from sqlalchemy.orm import *
from sqlalchemy  import *
engine=create_engine('sqlite:///new.db',echo=True)
meta=MetaData()

class User():
    user_table="user_account",
    id:Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[String] = mapped_column(String(30))
    age:Mapped[int] = mapped_column(nullable=False)

    Address:Mapped[list["address"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"id : {self.id} , name  : {self.name} , age : {self.age}"

class address():
    address_table= "address",
    id:Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[String] = mapped_column(String(100))
    user_id :Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user:Mapped["User"]  = relationship(back_populates="Address")

    def __repr__(self):
        return f"id : {self.id} , email :{self.email} , user_id  : {self.user_id}"

new_table=Table(
    "new_table" , meta,
    Column("id" , Integer , primary_key = True),
    Column("name"  ,String(30) , nullable=False),
    Column("age" , Integer , nullable=False)

)



# with Connection(engine) as con:
#     con.execute(
#         insert(new_table),[
#             {"id"  : 2 , "name"  : "kumar" , "age" : 22},
#             {"id"  : 3 , "name"  : "ak" , "age" : 33}
#         ]
#     )
#     con.commit()

# with engine.connect() as con:
#     result=con.execute(text("select id,name,age from new_table"))
#     for row in result:
#         print(f"id : {row.id}  , name : {row.name} , age : {row.age}")

# select_stmt = select(new_table).where(new_table.c.name=="arun")
# print(select_stmt.compile().params)
# with Connection(engine).execute(select_stmt) as stmt:
#     for row in stmt:
#         print(row)
user=123
a={"name" : "user", "id" : 2}
print(a["name"])