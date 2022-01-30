from sqlalchemy import Column, String, Integer

from db.dal import Base


class Artist(Base):
    __tablename__ = 'artists'

    id = Column('id', String(50), primary_key=True)
    name = Column('name', String(255), index=True)
    genre = Column('genre', String(100))
    image = Column('image', String(255))
    popularity = Column('popularity', Integer())

    def __repr__(self):
        return "<Artist(name='%s', genre='%s', image='%s', popularity='%s')>" % (
            self.name, self.genre, self.image, self.popularity)

    def __init__(self, artist_id, name, genre, image, popularity):
        self.id = artist_id
        self.name = name
        self.genre = genre
        self.image = image
        self.popularity = popularity
