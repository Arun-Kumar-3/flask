import requests
import json

base_url = "http://127.0.0.1:5000"

users=[
    { 'name' : 'arya' , 'age' : 11},
    { 'name' : 'vikram' , 'age' : 22},
    {'name' : 'vishal' , 'age' : 32},
    { 'name' : 'vijay' , 'age' : 44},
    { 'name' : 'ajith' , 'age' : 54},
]

for i in users:
    post_response=requests.post(base_url + "/user" , json=i)
    print(post_response.json())

input()

get_response=requests.get(base_url + "/user/2")
print(get_response.json())

input()
update= {'name' : 'mohanlal' , 'age' : 81 }
update_response=requests.put(base_url + "/user/3" , json=update )
print(update_response.json())

input()

delete_response=requests.delete(base_url + "/user/2")
print(delete_response.json())

input()

for i in range(1,20):
    all_users=requests.get(base_url + "/user/" + str(i))
    print(all_users.json())