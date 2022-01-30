import sqlalchemy
from pg8000 import Connection
from google.cloud.sql.connector import connector
from sqlalchemy.engine import Engine


def get_conn() -> Connection:
    conn: Connection = connector.connect("spotipy-echo-nest:us-central1:spotipy-artists", "pg8000",
                                         user="spotipy", password="C0d3M0nk3y", db="spotify")
    return conn


def get_pool_engine() -> Engine:
    pool = sqlalchemy.create_engine("postgresql+pg8000://", creator=get_conn)
    return pool

