import requests
from datetime import datetime
import pandas as pd

# Authentication credentials
CLIENT_ID = "YOvvbQxa9w2fbg4B2reO57im5vkn"
CLIENT_SECRET = "NBc6ffHzrm1QZvYdPCxDdlIM1v4X1Q"

# Function to obtain an access token
def get_token():
    req = requests.post(
        'https://api.soundcloud.com/oauth2/token',
        data={  # ✅ Use 'data' instead of 'params' for POST
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    )

    if req.status_code == 200:
        return req.json()
    else:
        print(f"❌ ERROR: Authentication failed - {req.status_code}")
        print(f"Response: {req.text}")
        return None

# Get authentication token
auth_data = get_token()

if auth_data and "access_token" in auth_data:
    token = auth_data['access_token']
    print("🔑 Token obtained:", token)
else:
    print("❌ ERROR: Failed to retrieve access token. Exiting.")
    exit()

# Function to fetch an artist's tracks
def get_artist_tracks(user_id):
    response = requests.get(
        f"https://api.soundcloud.com/users/{user_id}/tracks",
        headers={"Authorization": f"Bearer {token}"},
        params={"limit": 200}  # ✅ Fetch maximum number of tracks
    )

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ ERROR: Failed to fetch tracks for user {user_id} - {response.status_code}")
        print(f"Response: {response.text}")
        return None

# Function to convert a date into a week number
def get_week_from_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S%z")
    return date_obj.strftime("%Y-W%U")  # Year + Week Number

# Function to analyze weekly upload frequency
def analyze_upload_frequency(user_id):
    print("🚀 Starting Upload Frequency Analysis...")

    tracks = get_artist_tracks(user_id)
    if not tracks:
        print("⚠️ No tracks found.")
        return

    # Convert track data into a DataFrame
    track_data = []
    for track in tracks:
        created_at = track.get("created_at")
        if created_at:
            week = get_week_from_date(created_at)
            track_data.append({"artist_id": user_id, "week": week})

    df = pd.DataFrame(track_data)
    
    # Group by artist and week, count number of tracks released per week
    weekly_counts = df.groupby(["artist_id", "week"]).size().reset_index(name="track_count")

    # Calculate the average number of tracks released per week per artist
    artist_total_tracks = weekly_counts.groupby("artist_id")["track_count"].sum()
    artist_total_weeks = weekly_counts.groupby("artist_id")["week"].nunique()
    artist_avg_tracks_per_week = (artist_total_tracks / artist_total_weeks).reset_index()
    artist_avg_tracks_per_week.columns = ["artist_id", "avg_tracks_per_week"]

    # Display results
    print("\n📊 Weekly Upload Frequency:")
    print(weekly_counts)
    
    print("\n📊 Average Tracks Released per Week per Artist:")
    print(artist_avg_tracks_per_week)

# Example Usage (Replace with a real SoundCloud user ID)
USER_ID = "3207"  # Example ID (Deadmau5)
analyze_upload_frequency(USER_ID)
