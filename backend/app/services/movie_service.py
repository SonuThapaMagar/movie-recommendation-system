from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.movie import Movie

from app.services.tmdb_service import get_movie_details

# Convert SQLAlchemy Movie object into a Python dictionary
def _movie_to_dict(movie:Movie):
    # Get movie information from PostgreSQL
    movie_data={
        "movieId":movie.movie_id,
        "title":movie.title,
        "genres":movie.genres,
        
        "tmdb_id": movie.tmdb_id,
        "poster_url": movie.poster_url,
        "overview": movie.overview,
        "rating": movie.rating,
        "release_date": movie.release_date
    }
    
    if not movie.poster_url:
        details=get_movie_details(movie.title)
        if (details):
            movie_data.update(details)
        
    return movie_data

#Get all movies
def get_all_movies(db:Session,limit:int=20,skip:int=0,search:str|None=None,genre:str|None=None):
        
    query=db.query(Movie)
    
    #Search movie by title
    if search:query=query.filter(Movie.title.ilike(f"%{search}%"))
    
    #Filter movie by genre
    if genre:query=query.filter(Movie.genres.ilike(f"%{genre}%"))
        
    # Count matching movies before pagination.
    total_count=query.with_entities(func.count(Movie.movie_id)).scalar()
    
    # Apply sorting, skipping, and limiting
    movies=(query.order_by(Movie.movie_id).offset(skip).limit(limit).all())
    movie_data = [_movie_to_dict(movie) for movie in movies ]
        
    return {
        "count": total_count,
        "movies": movie_data
    }

#Get movie by id
def get_movie_by_id(db:Session,movie_id:int):
    
    movie=(db.query(Movie).filter(Movie.movie_id==movie_id).first())
    if movie is None: return None
    return _movie_to_dict(movie)