# Import necessary libraries:
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Import the credentials file to load the protected info:
import credentials as cr

# Function to find a playlist by name:
def find_playlist_by_name(sp, playlist_name):

    # Get all user playlists:
    playlists = []
    offset = 0
    
    # Paginate through playlists:
    while True:

        # Get a batch of playlists:
        results = sp.current_user_playlists(limit=50, offset=offset)

        # If no more playlists:
        if not results['items']:
            
            # Exit the loop:
            break
            
        # Add to the playlists list:
        playlists.extend(results['items'])

        # Update offset for next batch:
        offset += len(results['items'])
        
        # If the batch wasn't full:
        if len(results['items']) < 50:

            # Exit the loop:
            break
    
    # Search for the playlist by name:
    for playlist in playlists:

        # Check if the name matches:
        if playlist['name'] == playlist_name:

            # Return the playlist ID:
            return playlist['id']
    
    # If not found:
    return None

# Main function to update playlist from liked songs:
def update_playlist_from_liked_songs():

    # Set up cache directory:
    cache_path = os.path.join(os.getcwd(), '.spotify_cache')

    # If it doesn't exist:
    if not os.path.exists(cache_path):

        # Create it:
        os.makedirs(cache_path)

    # Spotify OAuth setup:
    scope = "user-library-read playlist-modify-public playlist-read-private"

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

    # Find the playlist:
    playlist_name = "EDM Gaming Mix"

    # Inform the user:
    print(f"Looking for playlist: {playlist_name}")

    # Get the playlist ID:    
    playlist_id = find_playlist_by_name(sp, playlist_name)

    # If not found:
    if not playlist_id:

        # Inform the user:
        print(f"Could not find playlist named '{playlist_name}'")
        return
    
    # Inform the user:
    print(f"Found playlist! ID: {playlist_id}")

    # Get all tracks in the playlist:
    playlist_tracks = []

    # Spotify API pagination variables:
    offset = 0

    # Set a loop:
    while True:

        # Get a batch of playlist tracks:
        results = sp.playlist_tracks(playlist_id, offset=offset)

        # If there are no more items:
        if not results['items']:

            # Exit the loop:
            break
        
        # Add to the playlist tracks list:
        playlist_tracks.extend(results['items'])

        # Update offset for next batch:
        offset += len(results['items'])

        # If the batch wasn't full:
        if len(results['items']) < 100:

            # Exit the loop:
            break

    # Inform the user:
    print(f"Found {len(playlist_tracks)} songs in current playlist")

    # Get liked songs until we find the most recent common song:
    print("Searching for the most recent common song...")
    
    # Spotify API pagination variables:
    offset = 0
    limit = 50
    found_common_song = False
    most_recent_common_song = None
    new_tracks = []

    # Set a loop:
    while not found_common_song:

        # Get a batch of liked songs:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)

        # If there are no more items:
        if not results['items']:

            # Exit the loop:
            break

        # Check each liked song:
        for liked_item in results['items']:

            # Get the liked track URI:
            liked_track_uri = liked_item['track']['uri']
            
            # Check if this liked song exists in playlist:
            for playlist_item in playlist_tracks:
                if playlist_item['track']['uri'] == liked_track_uri:
                    found_common_song = True
                    most_recent_common_song = liked_item['track']['name']
                    print(f"Found most recent common song: {most_recent_common_song}")
                    break
            
            # If not found yet:
            if not found_common_song:

                # This is a new song that should be added:
                track_name = liked_item['track']['name']
                artist_name = liked_item['track']['artists'][0]['name']
                print(f"Found new track: {track_name} by {artist_name}")
                new_tracks.append(liked_track_uri)

            # If found, break the outer loop as well:
            else:

                # Exit the for loop:
                break
                
        # Update offset for next batch:
        offset += limit

        # If the batch wasn't full:
        if len(results['items']) < limit:

            # Exit the loop:
            break

    # If no new tracks found:
    if not new_tracks:

        # Inform the user:
        print("No new songs to add!")
        return

    # Inform the user:
    print(f"\nAdding {len(new_tracks)} new songs to your playlist...")

    # Add new songs at the beginning of the playlist:
    sp.playlist_add_items(playlist_id, new_tracks, position=0)

    # Inform the user:
    print("Playlist successfully updated!")

# Run the main function:
if __name__ == "__main__":
    try:
        update_playlist_from_liked_songs()

    # Catch any exceptions:
    except Exception as e:
        print(f"An error occurred: {str(e)}")