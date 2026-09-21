import requests

url = "http://127.0.0.1:5000/api/weather"

params = {
    "city": "Goa"
}

response = requests.get(url, params=params)

print(response.status_code)
print(response.json())