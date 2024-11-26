import requests

endpoint ="http://localhost:8001/api/auth/login/"

data={
    "username": "vishal",
    "password": "qscwdv"
}
# Send a POST request
response = requests.post(endpoint, json=data)
print(response.status_code)
print(response.json())