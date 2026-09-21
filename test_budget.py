import requests

url = "http://127.0.0.1:5000/api/budget/plan"

data = {
    "destination": "Goa",
    "days": 3,
    "people": 2,
    "budget": 10000
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())