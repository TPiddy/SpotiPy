from sqlalchemy.engine import Engine
from sqlalchemy import text
from db_conn import get_pool_engine


def create():
    engine: Engine = get_pool_engine()

    artists_table = text(
        "CREATE TABLE IF NOT EXISTS artists (id VARCHAR(55) PRIMARY KEY, name VARCHAR(255), genres VARCHAR(255), image VARCHAR(100), popularity INTEGER)")
    tracks_table = text(
        "CREATE TABLE IF NOT EXISTS tracks (id VARCHAR(55) PRIMARY KEY, artist_id VARCHAR(55), CONSTRAINT artist FOREIGN KEY(artist_id) REFERENCES artists(id) ON DELETE CASCADE, name VARCHAR(255), duration INTEGER, acoustic DECIMAL, danceability DECIMAL, energy DECIMAL, instrumental DECIMAL, live DECIMAL, loudness DECIMAL, tempo DECIMAL, time_signature INTEGER)")
    with engine.connect() as connection:
        connection.execute(artists_table)
        connection.execute(tracks_table)

    engine.dispose()


if __name__ == "__main__":
    create()
