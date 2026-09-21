import requests

url = "http://127.0.0.1:5000/api/contact"

data = {
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Test Contact",
    "message": "This is a test message."
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:")

try:
    print(response.json())
except:
    print(response.text)