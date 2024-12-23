import requests

base_url ="http://127.0.0.1:5000"

post_response=requests.post("/data")
print(post_response.json())