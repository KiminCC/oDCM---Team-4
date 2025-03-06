import requests
import pandas as pd
import matplotlib.pyplot as plt

# Authentication credentials for SoundCloud API
CLIENT_ID = "tcgOlBvvbQxa9w2fbg4B2reO57im5vkn"
CLIENT_SECRET = "SUNBc6ffHzrm1QZvYdPCxDdlIM1v4X1Q"

def get_token():
    """Fetches an authentication token from the SoundCloud API."""
    req = requests.post(
        'https://api.soundcloud.com/oauth2/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }
    )
    if req.status_code == 200:
        return req.json().get('access_token')
    else:
        print(f"❌ Error getting token: {req.status_code}")
        exit()

# Get the authentication token
token = get_token()
print("🔑 Token obtained:", token)

# Endpoint to get data from Pro users and their tracks
API_URL = "http://127.0.0.1:5000/scrape_user_tracks"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Fetch data from the endpoint with the authentication header
response = requests.get(API_URL, headers=headers)
if response.status_code == 200:
    data = response.json().get("users_data", [])
    print(f"✅ Data received: {len(data)} users found.")
else:
    print(f"❌ Error fetching data: {response.status_code}")
    exit()

# Prepare data for analysis
all_tracks = []
for user_data in data:
    user_id = user_data.get("user_id")
    username = user_data.get("username")
    frequency = user_data.get("frequency", {})
    for date, count in frequency.items():
        all_tracks.append({
            "user_id": user_id,
            "username": username,
            "date": date,
            "track_count": count
        })

# Create a DataFrame from the collected data
df = pd.DataFrame(all_tracks)
if df.empty:
    print("⚠️ No data available for analysis.")
    exit()

# Display the DataFrame
print(df.head())

# Analyze the frequency of track publications
frequency_per_month = df.groupby("date")['track_count'].sum().reset_index()
frequency_per_month['date'] = pd.to_datetime(frequency_per_month['date'], format='%Y-%m')
frequency_per_month = frequency_per_month.sort_values('date')

# Plot the publication frequency
graph_title = 'Track Publication Frequency on SoundCloud'
plt.figure(figsize=(10, 6))
plt.plot(frequency_per_month['date'], frequency_per_month['track_count'], marker='o')
plt.xlabel('Date')
plt.ylabel('Number of Published Tracks')
plt.title(graph_title)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
