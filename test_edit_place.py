import requests

url = "http://127.0.0.1:5000/api/admin/places/1"

data = {
    "name": "Taj Mahal Updated",
    "location": "Agra, Uttar Pradesh",
    "category": "Historical",
    "description": "Updated tourist place description"
}

response = requests.put(url, json=data)

print(response.status_code)
print(response.json())