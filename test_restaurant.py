import requests

place_id = 1

url = f"http://127.0.0.1:5000/api/restaurants/{place_id}"

response = requests.get(url)

print("Status Code:", response.status_code)
print("Response:")

try:
    print(response.json())
except:
    print(response.text)