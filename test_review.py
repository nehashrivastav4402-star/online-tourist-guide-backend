import requests

url = "http://127.0.0.1:5000/api/reviews"

data = {
    "user_id": 1,
    "place_id": 1,
    "rating": 5,
    "comment": "Very beautiful place!"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())