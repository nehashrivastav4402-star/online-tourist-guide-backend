import requests

url = "http://127.0.0.1:5000/api/feedback"

data = {
    "user_id": 1,
    "message": "The tourist guide app is very useful."
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())