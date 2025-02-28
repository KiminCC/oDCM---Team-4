import requests

# Authentication credentials
CLIENT_ID = "tcgOlBvvbQxa9w2fbg4B2reO57im5vkn"
CLIENT_SECRET = "SUNBc6ffHzrm1QZvYdPCxDdlIM1v4X1Q"

def get_token():
    # Make a POST request to obtain the token
    req = requests.post(
        'https://api.soundcloud.com/oauth2/token',
        params={
            'Content-Type': 'application/x-www-form-urlencoded',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }
    )
    return req.json()

# Get the authentication token
auth_data = get_token()
token = auth_data['access_token']
print("Token:", token)

# Search for tracks using the query "lofi"
search_query = "lofi"
response = requests.get(
    "https://api.soundcloud.com/tracks",
    headers={"Authorization": f"Bearer {token}"},
    params={"q": search_query}
)

# Convert the response to JSON format
result = response.json()

# Print the result and its type
print("Result:", result)
print("Type of result:", type(result))

# If 'result' is a list, iterate over each element to print the track titles
if isinstance(result, list):
    for track in result:
        if isinstance(track, dict):
            title = track.get('title')
            print("Title:", title)
        else:
            print("Unexpected element:", track)
else:
    print("Unexpected response:", result)
