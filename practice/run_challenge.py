import json
import requests

base="http://127.0.0.1:5000"

employee_data =[
    {"name" : "vikram" , "age" : 11},
    {"name" : "vijay" , "age" : 21},
    {"name" : "rajini" , "age" : 31},
    {"name" : "ajith" , "age" : 41},
    {"name" : "ravi" , "age" : 51}
]


for em in employee_data:
    post=requests.post(base +"/employee" , json=em )
    print(post.json())

input()
for i in range(1,10):
    get=requests.get(base + '/employee/' +str(i))
    print(get.json())

input()
value={"name" : "arun" , "age" : 20}
update=requests.put( base + '/employee/3' , json=value)
print(update.json())

input()
patch_value={'name' : 'suriya'}
patch=requests.patch(base + '/employee/5' ,json=patch_value)
print(patch.json())

input()
delete=requests.delete(base + '/employee/4')
print(delete.json())

input()
for i in range(1,10):
    get=requests.get(base + '/employee/' +str(i))
    print(get.json())

input()

import requests

# Flask server endpoint
# Replace this with your actual Flask route

# Sending a HEAD request to the server
response = requests.head(base + '/employee')

# Print the status code of the response
print("Status Code:", response.status_code)

# Print the response headers
print("Response Headers:", response.headers)

# If you need a specific header value, you can access it like this:
if 'Custom-Header' in response.headers:
    print("Custom-Header:", response.headers['Custom-Header'])

input()

input()
response = requests.options(base + '/employee')
print(response.json())
