from sqlalchemy import Float, Boolean
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from typing import Optional

BaseMovies = declarative_base()


class DirectorEntity(BaseMovies):
    __tablename__ = "directors"
    id = Column(Integer, Sequence("director_sequence"), primary_key=True)
    name = Column(String, index=True, nullable=False)
    birth_date = Column(String)
    country = Column(String)
    movies = relationship("MovieEntity", back_populates="director")


# Режиссер
class MovieEntity(BaseMovies):
    __tablename__ = "movies"
    id = Column(Integer, Sequence("movie_sequence"), primary_key=True)
    title = Column(String, index=True, nullable=False)
    release_year = Column(Integer)
    genre = Column(String)
    rating = Column(Float)
    is_published = Column(Boolean, default=True)
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=True)
    director = relationship("DirectorEntity", back_populates="movies")


class Director(BaseModel):
    id: int
    name: str
    birth_date: str
    country: int


class Movie(BaseModel):
    id: int
    title: str
    release_year: int
    genre: str
    rating: float
    is_published: bool
    director_id: Optional[int]
