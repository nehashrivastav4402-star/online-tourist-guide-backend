import requests

url = "http://127.0.0.1:5000/api/register"

data = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "test123"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())