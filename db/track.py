from sqlalchemy import Column, String, ForeignKey, Integer, Numeric

from db.dal import Base


class Track(Base):
    __tablename__ = 'tracks'

    id = Column('id', String(50), primary_key=True)
    name = Column('name', String(255), index=True)
    artist_id = Column('artist_id', String(100),
                       ForeignKey('artists.id', None, False, 'artist', None, 'CASCADE'), nullable=False)
    duration = Column('duration', Integer()),
    acoustic = Column('acoustic', Numeric(12, 2)),
    energy = Column('energy', Numeric(12, 2)),
    danceability = Column('danceability', Numeric(12, 2)),
    live = Column('live', Numeric(12, 2)),
    instrumental = Column('instrumental', Numeric(12, 2)),
    loudness = Column('loudness', Numeric(12, 2)),
    tempo = Column('tempo', Numeric(12, 2)),
    time_signature = Column('time_signature', Integer())

    def __repr__(self):
        return "<Track(name='%s', artist_id='%s', duration='%s', acoustic='%s', " \
               "energy='%s', danceability='%s', live='%s', instrumental='%s'," \
               "loudness='%s', tempo='%s' time_signature='%s')>" % (
                   self.name, self.artist_id, self.duration, self.acoustic, self.energy,
                   self.danceability, self.live, self.instrumental, self.loudness, self.tempo, self.time_signature)

    def __init__(self, track_id, name, artist_id):
        self.id = track_id
        self.name = name
        self.artist_id = artist_id
