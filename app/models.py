from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False, index=True)
    year = Column(Integer, nullable=True, index=True)
    genre = Column(String(300), nullable=True, index=True)
    rating = Column(Float, nullable=True, index=True)
    director = Column(String(500), nullable=True)
    cast = Column(Text, nullable=True)
    runtime = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    poster_url = Column(String(1000), nullable=True)
    source_url = Column(String(1000), nullable=True, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
