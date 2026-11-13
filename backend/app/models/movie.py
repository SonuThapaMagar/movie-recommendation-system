from sqlalchemy import Column,Integer,String, Float,Text
from sqlalchemy.orm import relationship
from app.database.database import Base

class Movie(Base):
    __tablename__ = "movies"
    
    # Primary key from MovieLens
    movie_id=Column(Integer,primary_key=True,index=True)
    
    #Movie information
    title=Column(String(255),nullable=False)
    genres=Column(String(255),nullable=True)
    
    #TMDB Information
    tmdb_id=Column(Integer, nullable=True,index=True)
    poster_url=Column(Text,nullable=True)
    overview=Column(Text,nullable=True)
    rating=Column(Text,nullable=True)
    release_date=Column(String(20),nullable=True)
    
    # Relationships
    ratings=relationship("Rating",back_populates="movie")
    tags=relationship("MovieTag",back_populates="movie")