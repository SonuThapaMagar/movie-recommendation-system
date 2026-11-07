from pathlib import Path
import pandas as pd

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
    
    movies=df.head(limit)
    
    # Converts rows into dictionaries so FastAPI can return as JSON
    return movies.to_dict(orient="records")
