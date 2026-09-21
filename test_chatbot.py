import requests

url = "http://127.0.0.1:5000/api/chatbot"

data = {
    "message": "Best tourist places in Goa?"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())