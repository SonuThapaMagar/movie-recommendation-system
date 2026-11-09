import os
import re
import httpx

from dotenv import load_dotenv
from functools import lru_cache

# Load environment variables
load_dotenv()

#TMDB Configuration
TMDB_API_KEY=os.getenv("TMDB_API_KEY")

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

@lru_cache(maxsize=1000)
def get_movie_details(title:str):
    """
    Search TMDB using a MovieLens movie title.
    Cache results to avoid repeating the same API request.
    """
    if not TMDB_API_KEY:
        return None
    
    # Extract the release year from titles like Toy Story (1995)
    year_match=re.search(r"\((/d{4})\)$",title)
    search_title=re.sub(r"\s*\(\d{4}\)$","",title).strip()
    
    params={
        "api_key":TMDB_API_KEY,
        "query":search_title
    }
    
    # Include the release year when available
    if(year_match):
        params["year"]=year_match.group(1)
        
    try:
        response=httpx.get(f"{TMDB_BASE_URL}/search/movie",params=params,timeout=10.0)
        response.raise_for_status()
        results=response.json().get("results",[])
        
        if not results:
            return None
        
        #Get the first moving movie
        movie=results[0]
        poster_path=movie.get("poster_path")
        if not poster_path:
            return None
        
        return {
            "tmdb_id": movie.get("id"),
            "poster_url": (
                f"{TMDB_IMAGE_URL}{poster_path}"
                if poster_path
                else None
            ),
            "rating": movie.get("vote_average"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
        }
    
    except httpx.HTTPError as error:
        print(f"TMDB request failed for {title}:{error}")
        return None