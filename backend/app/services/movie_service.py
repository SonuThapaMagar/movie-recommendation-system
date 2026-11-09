from pathlib import Path
import pandas as pd

from app.services.tmdb_service import get_movie_details

# Movie dataset
DATA_PATH=Path(__file__).resolve().parents[2]/"data"/"movies.csv"

#Loading movie data
def load_movies():
    df=pd.read_csv(DATA_PATH)
    
    # Handle missing vaues
    df['genres']=df['genres'].fillna("")
    
    return df

#Get all movies
def get_all_movies(limit=20):
    
    df=load_movies()
    
    movies=df.head(limit).to_dict(orient="records")
    
    for movie in movies:
        details=get_movie_details(movie["title"])
        
        # TMDB details to MovieLens data
        movie.update(
            details or {
                "tmdb_id":None,
                "poster_url":None,
                "rating":None,
                "overview":None,
                "release_date":None
            }
        )
    
    # Converts rows into dictionaries so FastAPI can return as JSON
    return movies
