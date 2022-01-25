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
        tracks = spotify.playlist_items(playlist['id'],
                                        'items(track(name,href,artists(name,id)))', 100, 0, None,
                                        ['track'])
        for track in tracks['items']:
            artists.append(track['track']['artists'][0])

    return artists


def update_artist_records(spotify, artists):
    engine: Engine = get_pool_engine()
    with engine.connect() as connection:
        for artist in artists:
            artist_data = spotify.artist(artist['id'])
            statement = text("INSERT INTO artists (id, name, genres, image, popularity) "
                             "VALUES (:id, :name, :genres, :image, :popularity)")
            connection.execute(statement,
                               {"id": artist_data['id'],
                                "name": artist_data['name'],
                                "genres": ''.join(artist_data['genres']),
                                "image": artist_data['images'][0].url,
                                "popularity": artist_data['popularity']})
    engine.dispose()


if __name__ == "__main__":
    main()