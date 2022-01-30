from google.cloud.sql.connector import connector
from psycopg2 import connection
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

Base = declarative_base()


class DataAccessLayer:
    connection: connection = None
    engine: Engine = None

    def create_session(self, user, password) -> Session:
        self.connection = connector.connect("spotipy-echo-nest:us-central1:spotipy-artists", "psycopg2",
                                            user=user, password=password, db="spotify")
        self.engine = create_engine("postgresql+psycopg2://", creator=self.connection)
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        return session()

