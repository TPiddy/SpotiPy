import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from db.artist import Artist
from db.dal import DataAccessLayer
from db.track import Track


def spotify_import():
    dal = DataAccessLayer()
    session = dal.create_session(os.environ.get('DB_USER'), os.environ.get('DB_PASS'))
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    artists = get_artists(spotify)
    for artist in create_artist_records(spotify, artists):
        session.add(artist)
    for track in create_tracks(spotify, artists):
        session.add(track)

    session.commit()
    session.close()


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


def create_artist_records(spotify, artists):
    artist_records = []
    for artist in artists:
        artist_data = spotify.artist(artist['id'])
        artist_records.append(Artist(
            artist_data['id'],
            artist_data['name'],
            artist_data['genres'][0] if len(artist_data['genres']) else 'N/A',
            artist_data['images'][0]['url'] if len(artist_data['images']) else None,
            artist_data['popularity']
        ))
    return artist_records


def create_tracks(spotify, artists):
    track_records = []
    for artist in artists:
        tracks = spotify.artist_top_tracks(artist['id'])
        tracks_meta = spotify.audio_features(tracks)
        for idx, track in enumerate(tracks):
            track_meta = tracks_meta[idx]
            if track_meta is None:
                continue
            record = Track(track['id'], track['name'], artist['id'])
            record.duration = track_meta['duration'],
            record.acoustic = track_meta['acoustic'],
            record.danceability = track_meta['danceability'],
            record.energy = track_meta['energy'],
            record.instrumental = track_meta['instrumental'],
            record.live = track_meta['live'],
            record.loudness = track_meta['loudness'],
            record.tempo = track_meta['tempo'],
            record.time_signature = track_meta['time_signature']
            track_records.append(record)

    return track_records


if __name__ == "__main__":
    spotify_import()
