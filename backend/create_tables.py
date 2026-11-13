from app.database.database import Base,engine

# All models
from app.models.user import User
from app.models.movie import Movie
from app.models.rating import Rating
from app.models.movie_tag import MovieTag

# Create database tables
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
