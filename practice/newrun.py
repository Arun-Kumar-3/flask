import requests

base_url="http://127.0.0.1:5000"

#response_get=requests.get(base_url + "/data/new name",{"likes" : 100})
#response_post=requests.post(base_url + "/data/new")

#print(f"this is get response :  {response_get.json()}")
#print(f"this is post response : {response_post.json()}")

#response_put=requests.put(base_url + "/data/1", json={"likes" : 10000 })

#print(response_put.json())

#get_id=requests.get(base_url + "/data/2")
#print(get_id.json())


data=[
    {"likes" : 1000  ,"viwes" : 100000  ,"dislikes" : 100},
    {"likes" : 2000  ,"viwes" : 200000  ,"dislikes" : 200},
    {"likes" : 3000  ,"viwes" : 300000  ,"dislikes" : 300},
    {"likes" : 4000  ,"viwes" : 400000  ,"dislikes" : 400},
    {"likes" : 5000  ,"viwes" : 500000 ,"dislikes" : 500},
]

for i in range(len(data)):
    response_put=requests.put(base_url + "/data/" +str(i) ,json=data[i])
    print(response_put.json())
input()
del_response=requests.delete(base_url + "/data/1")
print(del_response)
input()
for j in range(len(data)):
    get_response=requests.get(base_url + "/data/" + str(j))
    print(get_response.json())