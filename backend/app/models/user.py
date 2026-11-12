from datetime import datetime, timezone
from sqlalchemy import Column,DateTime, Integer, String
from app.database.database import Base

class User(Base):
    __tablename__ = "users"
    
    # Primary key
    id=Column(Integer,primary_key=True,index=True)
    
    # User information
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    # Store hashed password, never plain-text password
    hashed_password = Column(String(255), nullable=False)

    # Account creation time
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )