import requests

# Replace with your actual token
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

# API endpoint to get user info
url = "https://api.soundcloud.com/me"

# Headers with the access token
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Accept": "application/json; charset=utf-8"
}

# Make the request
response = requests.get(url, headers=headers)

# Print the response JSON
print(response.json())




