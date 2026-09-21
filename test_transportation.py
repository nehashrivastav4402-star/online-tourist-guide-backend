import requests

url = "http://127.0.0.1:5000/api/transportation/1"

response = requests.get(url)

print(response.status_code)
print(response.json())