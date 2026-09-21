import requests

url = "http://127.0.0.1:5000/api/voice-search"

data = {
    "query": "Taj Mahal"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())