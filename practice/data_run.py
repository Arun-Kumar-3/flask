import requests

base_url = "http://127.0.0.1:5000"

datas=[
    {"name" : "vikram" , "age" :41 , "city" : "chennai"},
    {"name" : "ajith" , "age" :70 , "city" : "gova"},
    {"name" : "vijay" , "age" :41 , "city" : "madurai"},
    {"name" : "rajini" , "age" :68 , "city" : "coimbatore"},
]

for i in range(len(datas)):
    put_response=requests.put(base_url + "/data/" + str(i), json=datas[i])
    print(put_response.json())

input()

post_response=requests.post(base_url + "/data/3")
print(post_response.json())

input()

del_response=requests.delete(base_url + "/data/2")
print(del_response.json())

input()
for j in range(len(datas)):
    get_response=requests.get(base_url + "/data/" + str(j))
    print(get_response.json())

