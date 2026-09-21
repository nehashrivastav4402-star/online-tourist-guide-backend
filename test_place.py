import requests

url = "http://127.0.0.1:5000/api/places"

data = {
    "name": "Gateway of India",
    "description": "A famous tourist attraction in Mumbai.",
    "location": "Mumbai",
    "category": "Historical",
    "image_url": ""
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())