import json
import pandas as pd
import matplotlib.pyplot as plt

# Load data from JSON file
file_path = "/Users/beatrice/oDCM---Team-4-1/soundcloud_data.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare data for analysis
tracks = []
for user in data['users_data']:
    for track in user['tracks']:
        tracks.append({
            'artist': user['username'],
            'track_title': track.get('title'),
            'created_at': track.get('created_at'),
            'playback_count': track.get('playback_count', 0),
            'playlist_count': user.get('frequency', {}).get('playlist_count', 0)
        })

df = pd.DataFrame(tracks)

print("\n🎵 Number of tracks per artist:\n")
tracks_per_artist = df['artist'].value_counts()
print(tracks_per_artist)

# Plot the number of tracks per artist
plt.figure(figsize=(12, 6))
tracks_per_artist.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Number of Tracks per Artist', fontsize=16)
plt.xlabel('Artist', fontsize=14)
plt.ylabel('Number of Tracks', fontsize=14)
plt.xticks(rotation=90, fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# Calculate upload frequency per artist
df['created_at'] = pd.to_datetime(df['created_at'], format='%Y/%m/%d %H:%M:%S %z', errors='coerce')
df['month'] = df['created_at'].dt.to_period('M')
upload_frequency = df.groupby(['artist', 'month']).size().reset_index(name='uploads')

print("\n📅 Upload frequency per artist:\n")
print(upload_frequency)

# Plot upload frequency per artist
for artist in upload_frequency['artist'].unique():
    artist_data = upload_frequency[upload_frequency['artist'] == artist]
    plt.figure(figsize=(8, 4))
    plt.plot(artist_data['month'].astype(str), artist_data['uploads'], marker='o', linestyle='-', color='orange')
    plt.title(f'Upload Frequency for {artist}', fontsize=14)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Uploads', fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Analyze the influence of upload frequency and playlist appearances on play count
correlation_data = df.groupby('artist').agg({
    'playback_count': 'sum',
    'track_title': 'count',
    'playlist_count': 'sum'
}).reset_index()
correlation_data.columns = ['Artist', 'Total Plays', 'Total Uploads', 'Playlist Appearances']

print("\n📈 Correlation Analysis:\n")
print(correlation_data)

# Plot correlation between upload frequency and playback count
plt.figure(figsize=(10, 6))
scatter = plt.scatter(correlation_data['Total Uploads'], correlation_data['Total Plays'], 
                      c=correlation_data['Playlist Appearances'], cmap='viridis', alpha=0.7, edgecolors='w', linewidth=0.5)
plt.colorbar(scatter, label='Playlist Appearances')
plt.xlabel('Total Uploads', fontsize=14)
plt.ylabel('Total Plays', fontsize=14)
plt.title('Influence of Upload Frequency on Play Count', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
