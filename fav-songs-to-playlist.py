# Import necessary libraries:
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Import the credentials file to load the protected info:
import credentials as cr

# Main function:
def create_playlist_from_liked_songs():

    # Set up cache directory:
    cache_path = os.path.join(os.getcwd(), '.spotify_cache')

    # If it doesn't exist:
    if not os.path.exists(cache_path):

        # Create it:
        os.makedirs(cache_path)

    # Spotify OAuth setup:
    scope = "user-library-read playlist-modify-public"

    # Initialize Spotify client with OAuth:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(

        # Define the scope:
        scope=scope,

        # Load the secret values:
        client_id=cr.CLIENT_ID,
        client_secret=cr.CLIENT_SECRET,
        redirect_uri=cr.REDIRECT_URL,

        # Set cache path:
        cache_path=os.path.join(cache_path, '.spotify_token_cache')
    ))

    # Get user ID:
    user_id = sp.current_user()['id']

    # Create new playlist:
    playlist = sp.user_playlist_create(

        # Define user ID:
        user_id,

        # Give it any name you want:
        name="My Liked Songs Playlist 2",

        # Add a description:
        description="Automatically generated from my Liked Songs"
    )

    # Get the playlist ID:
    playlist_id = playlist['id']

    # Get all liked songs:
    liked_songs = []

    # Spotify API pagination variables:
    offset = 0
    limit = 50

    # Inform the user:
    print("Fetching your liked songs...")

    # Set a loop:
    while True:

        # Get a batch of liked songs:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)

        # If there are no more items:
        if not results['items']:

            # Exit the loop:
            break
        
        # Extract track URIs:
        track_uris = [item['track']['uri'] for item in results['items']]

        # Add to the liked songs list:
        liked_songs.extend(track_uris)

        # Update offset for next batch:
        offset += limit

        # Print progress:
        print(f"Found {len(liked_songs)} songs so far...")

        # If the batch wasn't full:
        if len(results['items']) < limit:

            # Exit the loop:
            break

    # Inform the user:
    print(f"\nAdding {len(liked_songs)} songs to your new playlist...")

    # Add songs to new playlist

    # Set batch size (Spotify has a limit of 100 tracks per request):
    batch_size = 100

    # Loop through liked songs in batches:
    for i in range(0, len(liked_songs), batch_size):

        # Get the current batch:
        batch = liked_songs[i:i + batch_size]

        # Add the batch to the playlist:
        sp.playlist_add_items(playlist_id, batch)

        # Print progress:
        print(f"Added songs {i+1} to {min(i+batch_size, len(liked_songs))}")

    # Return the playlist URL:
    return playlist['external_urls']['spotify']

# Run the main function:
if __name__ == "__main__":
    try:

        # Call the function:
        playlist_url = create_playlist_from_liked_songs()

        # Print the playlist URL:
        print(f"\nSuccess! Your new playlist is available at: {playlist_url}")

    # Catch any exceptions:
    except Exception as e:
        print(f"An error occurred: {str(e)}")