import spotipy
from sqlalchemy.engine import Engine
from sqlalchemy import text
from spotipy.oauth2 import SpotifyClientCredentials
from db_conn import get_pool_engine


def main():
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    artists = get_artists(spotify)
    update_artist_records(spotify, artists)


def get_artists(spotify):
    artists = []
    playlists = spotify.category_playlists('toplists')
    for playlist in playlists['playlists']['items']:
        tracks = spotify.playlist_items(playlist['id'], 'items(track(name,href,artists(name,id)))', 100, 0, None,
                                        ['track'])
        for track in tracks['items']:
            artists.append(track['track']['artists'][0])

    return artists


def update_artist_records(spotify, artists):
    pool: Engine = get_pool_engine()
    pool.connect()
    for artist in artists:
        artist_data = spotify.artist(artist['id'])
        statement = text()
        pool.execute()


if __name__ == "__main__":
    main()