import requests

base_url = "http://127.0.0.1:5000"

response_get=requests.get(base_url + "/video/1")
print(response_get)