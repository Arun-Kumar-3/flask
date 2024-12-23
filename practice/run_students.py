import requests

base_url="http://127.0.0.1:5000"

student_data=[
    {"name" : "arya" , "age" : 10 , "city" : "chennai"},
    {"name" : "vikram" , "age" : 60 , "city" : "vada chennai"},
    {"name" : "sanjay" , "age" : 12 , "city" : "madurai"},
    {"name" : "dhoni" , "age" : 43 , "city" : "coimbatore"},
    {"name" : "virat" , "age" : 38 , "city" : "banglore"},
    {"name" : "rohit" , "age" : 41 , "city" : "cochin"},
    

]

for i in range(len(student_data)):
    put_req=requests.put(base_url + "/students/" + str(i) , student_data[i])
    print(put_req.json())

input()





del_req=requests.delete(base_url + "/students/2")
print(del_req)

input()

for j in range(len(student_data)):
    get_req=requests.get(base_url + "/students/" + str(j))
    print(get_req)

input()
post_req=requests.post(base_url + "/students/4")
print(post_req.json())

input()
for j in range(len(student_data)):
    get_req=requests.get(base_url + "/students/" + str(j))
    print(get_req)