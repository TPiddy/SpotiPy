import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sqlalchemy import text
from sqlalchemy.engine import Engine

from db_conn import get_pool_engine


def main():
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    artists = get_artists(spotify)
    update_artist_records(spotify, artists)
    update_tracks(spotify, artists)


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
                             "VALUES (:id, :name, :genres, :image, :popularity)"
                             "ON CONFLICT (id) DO UPDATE SET popularity = EXCLUDED.popularity")
            connection.execute(statement,
                               {"id": artist_data['id'],
                                "name": artist_data['name'],
                                "genres": artist_data['genres'][0] if len(artist_data['genres']) else 'N/A',
                                "image": artist_data['images'][0]['url']if len(artist_data['images']) else None,
                                "popularity": artist_data['popularity']})
    engine.dispose()


def update_tracks(spotify, artists):
    engine: Engine = get_pool_engine()
    with engine.connect() as connection:
        for artist in artists:
            tracks = spotify.artist_top_tracks(artist['id'])
            tracks_meta = spotify.audio_features(tracks)
            for idx, track in enumerate(tracks):
                track_meta = tracks_meta[idx]
                if track_meta is None:
                    continue
                statement = text(
                    "INSERT INTO tracks(id, artist_id, name, duration, acoustic, danceability, energy, instrumental, live, loudness, tempo, time_signature)"
                    "VALUES (:id, :artist_id, :name, :duration, :acoustic, :danceability, :energy, :instrumental, :live, :loudness, :tempo, :time_signature)"
                    "ON CONFLICT(id) DO NOTHING")
                print("track, track meta", track, track_meta)
                connection.execute(statement,
                                   {"id": track['id'],
                                    "name": track['name'],
                                    "artist_id": artist['id'],
                                    "duration": track_meta['duration'],
                                    "acoustic": track_meta['acoustic'],
                                    "danceability": track_meta['danceability'],
                                    "energy": track_meta['energy'],
                                    "instrumental": track_meta['instrumental'],
                                    "live": track_meta['live'],
                                    "loudness": track_meta['loudness'],
                                    "tempo": track_meta['tempo'],
                                    "time_signature": track_meta['time_signature']})
    connection.close()


if __name__ == "__main__":
    main()
