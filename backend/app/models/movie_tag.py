from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class MovieTag(Base):
    __tablename__="movie_tags"
    
    movie_tag_id=Column(Integer,primary_key=True,nullable=False, index=True)
    
    dataset_user_id = Column(Integer, nullable=False, index=True)
    
    movie_id=Column(Integer,ForeignKey="movies.movie_id",nullable=False,index=True)
    
    tag=Column(String(255),nullable=False)
    
    timestamp = Column(BigInteger, nullable=True)

    movie = relationship("Movie", back_populates="tags")
