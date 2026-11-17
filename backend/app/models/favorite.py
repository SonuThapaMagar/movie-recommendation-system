from datetime import datetime,timezone
from sqlalchemy import(Column,Integer,DateTime,ForeignKey,UniqueConstraint)
from sqlalchemy.orm import relationship

from app.database.database import Base

class Favorite(Base):
    __tablename__="favorites"
    
    __table_args__ = (
    UniqueConstraint(
        "user_id",
        "movie_id",
        name="uq_user_movie_favorite"
    ),
)
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False,index=True)
    
    movie_id=Column(Integer,ForeignKey("movies.movie_id"),nullable=False,index=True)
    
    created_at = Column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
    
    user=relationship("User")
    movie=relationship("Movie")