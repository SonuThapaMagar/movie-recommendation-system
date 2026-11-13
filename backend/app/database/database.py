import os
from dotenv import load_dotenv
from sqlalchemy import create_engine #Establishes db connectivity
from sqlalchemy.orm import declarative_base,sessionmaker #sessionmaker=Creates database sessions

#Load env
load_dotenv()

#Postgres SQL Connection
DATABASE_URL=os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE URL is not configured")

# Create database engine
engine=create_engine(DATABASE_URL,pool_pre_ping=True)

#Create db session factory
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base class for database models base=Parent class for database models
Base = declarative_base()

# Provide a database session to API routes
def get_db():
    db=SessionLocal()
    
    try:
        yield db
    finally:
        db.close()