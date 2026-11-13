from sqlalchemy import Column,Integer,Float, BigInteger,ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Rating(Base):

    __tablename__ = "ratings"
    
    rating_id=Column(Integer,primary_key=True,index=True)
    
    # Original MovieLens user ID
    dataset_user_id=Column(Integer,nullable=False,index=True)
    
    #Movie relationship
    movie_id=Column(Integer,ForeignKey("movies.movie_id"),nullable=False,index=True)
    
    #User's movie rating
    rating = Column(Float, nullable=False)
    timestamp = Column(BigInteger, nullable=True)
    
    # Relationship
    movie=relationship("Movie",back_populates="ratings")