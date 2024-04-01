def add_to_playlist(track_uri, playlist_id, sp):
    track_uri = "spotify:track:" + track_uri
    sp.playlist_add_items(playlist_id, [track_uri])

def get_songs_from_collection(playlist_id, sp):
    limit = 50
    offset = 0
    all_tracks = []
    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        tracks = results['items']
        if not tracks:
            break
        all_tracks.extend(tracks)
        offset += limit

    liked_dates = [datetime.strptime(item['added_at'], '%Y-%m-%dT%H:%M:%SZ') for item in all_tracks]

    sorted_indices = sorted(range(len(liked_dates)), key=lambda k: liked_dates[k])

    for i in sorted_indices:
        track_info = all_tracks[i]['track']
        track_id = track_info['id']
        track_name = track_info['name']
        liked_date = liked_dates[i].strftime('%Y-%m-%d')
        add_to_playlist(track_id, playlist_id, sp)
        print(f"Track ID: {track_id} - Track Name: {track_name} - Liked Date: {liked_date}")
        sleep(1)


import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from time import sleep

client_id = "014954a55b6549a1ae077a311a2d178f"
client_secret = "4f43edbcf9c6466784272fbdf05b9c20"
redirect_uri = "http://localhost:5000/callback"
scope='playlist-modify-public playlist-read-private user-library-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))
get_songs_from_collection("01LBlvmkTPFZh9SNGqMVhl", sp)
