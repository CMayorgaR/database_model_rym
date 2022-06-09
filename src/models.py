import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from eralchemy import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user_email = Column(String(25))
    user_password = Column(String(20))
    favorites = relationship("Favorites")


class Favorites(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    character = relationship(
        "Character", back_populates="favorites", uselist=False)
    location = relationship(
        "Location", back_populates="favorites", uselist=False)
    episode = relationship(
        "Episode", back_populates="favorites", uselist=False)


character_episode = Table(
    "association",
    Base.metadata,
    Column("character_id", ForeignKey("character.id"), primary_key=True),
    Column("episode_id", ForeignKey("episode.id"), primary_key=True),
)

class Character(Base):
    __tablename__ = "character"
    id = Column(Integer, primary_key=True)
    character_name = Column(String(20))
    character_status = Column(String(20))
    character_species = Column(String(20))
    character_origin = Column(String(20))
    favorites_id = Column(Integer, ForeignKey("favorites.id"))
    location = relationship("Location", back_populates="character")
    episode = relationship(
        "Episode", secondary=character_episode, back_populates="character")

class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    location_name = Column(String(30))
    location_type = Column(String(30))
    favorites_id = Column(Integer, ForeignKey("favorites.id"))
    character_id = Column(Integer, ForeignKey("character.id"))
    character = relationship("Character", back_populates="location")
    episode = relationship("Episode")
    episode_id=Column(Integer, ForeignKey("episode.id"))


class Episode(Base):
    __tablename__ = "episode"
    id = Column(Integer, primary_key=True)
    episode_name = Column(String(30))
    episode_air_date = Column(String(20))
    favorites_id = Column(Integer, ForeignKey("favorites.id"))
    character = relationship(
        "Character", secondary=character_episode, back_populates="episode")
    location_id= Column(Integer, ForeignKey("location.id"))
    location = relationship("Location")

    def to_dict(self):
        return {}


# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
