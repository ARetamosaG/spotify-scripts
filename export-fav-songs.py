# Import necessary libraries:
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from datetime import datetime

# Import the credentials file to load the protected info:
import credentials as cr

# Main function:
def export_liked_songs_to_txt():

    # Generate timestamped filename:
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M")
    filename = f"liked_songs_{timestamp}.txt"

    # Authentication setup:
    cache_path = os.path.join(os.getcwd(), '.spotify_cache')
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    # Spotify OAuth setup:
    scope = "user-library-read"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=cr.CLIENT_ID,
        client_secret=cr.CLIENT_SECRET,
        redirect_uri=cr.REDIRECT_URL,
        cache_path=os.path.join(cache_path, '.spotify_token_cache')
    ))

    # Initialize variables:
    liked_songs = []
    offset = 0
    limit = 50

    # Inform the user:
    print("Retrieving fav songs...")

    # Loop to get all liked songs:
    while True:

        # Get a batch of liked songs:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if not results['items']:
            break

        # Process each liked song:
        for item in results['items']:
            track = item['track']
            song_name = track['name']
            artists = ', '.join([artist['name'] for artist in track['artists']])
            liked_songs.append(f"{song_name} - {artists}")

        # Update offset for next batch:
        offset += limit
        if len(results['items']) < limit:
            break

    # Write to the file:
    with open(filename, "w", encoding="utf-8") as f:
        for line in liked_songs:
            f.write(line + "\n")

    # Inform the user:
    print(f"Export finished. Fav songs saved in: {filename}")

# Run the main function:
if __name__ == "__main__":
    try:
        export_liked_songs_to_txt()

    # Catch any exceptions:
    except Exception as e:
        print(f"An error occurred: {str(e)}")
