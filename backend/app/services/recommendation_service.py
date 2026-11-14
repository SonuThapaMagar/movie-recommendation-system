import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.models.movie_tag import MovieTag
from app.services.movie_service import get_movie_details

def prepare_movie_data(db:Session):
    #Fetch all movies
    movies=db.query(Movie).all()
    
    # Fetch all movie tags
    tags=db.query(MovieTag).all()
    
    # Convert movie tag into dictionary
    movie_tags={}
    
    for tag in tags:
        if tag.movie_id not in movie_tags:
            movie_tags[tag.movie_id]=[]
            
        movie_tags[tag.movie_id].append(tag.tag)
    #Movie info
    movie_data=[]
    
    for movie in movies:
        #Movie genres
        genres=(movie.genres or "").replace("|"," ")
        
        #Get tags associated with movie
        tags_text=" ".join(movie_tags.get(movie.movie_id,[]))
        
        #combine genres and tags
        combined_features = f"{genres} {tags_text}".strip()
        
        movie_data.append({
            "movie_id": movie.movie_id,
            "title": movie.title,
            "genres": genres,
            "tags": tags_text,
            "poster_url": movie.poster_url,
            "combined_features": combined_features
        })
        
    df=pd.DataFrame(movie_data)
    return df

#TF-IDF Vectorization of movie genres and tags
def create_tfidf_matrix(df):
    tfidf=TfidfVectorizer(stop_words="english") #stop words "the", "is", and "and" is removed
    
    # Convert movie text features into numerical vectors
    tfidf_matrix=tfidf.fit_transform(df["combined_features"])
    
    return tfidf,tfidf_matrix

#find movie similar to selected movie
def get_movie_recommendations(db, movie_id, top_n=10):
    df = prepare_movie_data(db)

    if df.empty:
        return []

    # Generate TF-IDF vectors
    _, tfidf_matrix = create_tfidf_matrix(df)

    # Find the selected movie's DataFrame index
    movie_indices = df.index[
        df["movie_id"] == movie_id
    ].tolist()

    if not movie_indices:
        return None

    movie_index = movie_indices[0]

    # Calculate similarity with all movies
    similarity_scores = linear_kernel(
        tfidf_matrix[movie_index],
        tfidf_matrix
    ).flatten()

    # Sort movies by similarity (highest first)
    similar_indices = similarity_scores.argsort()[::-1]

    recommendations = []
    updated_posters = False

    for index in similar_indices:

        # Do not recommend the selected movie itself
        if index == movie_index:
            continue

        recommended_movie_id = int(
            df.iloc[index]["movie_id"]
        )
        
        # Get movie from database
        movie = db.query(Movie).filter(
            Movie.movie_id == recommended_movie_id
        ).first()
        poster_url = movie.poster_url if movie else None
        
        # Fetch poster from TMDB
        if movie and not poster_url:
            details = get_movie_details(movie.title)
            if details:
                poster_url = details.get("poster_url")
                
                # Save poster URL in database
                if poster_url:
                    movie.poster_url = poster_url
                    updated_posters = True
        recommendations.append({
            "movie_id": int(df.iloc[index]["movie_id"]),
            "title": df.iloc[index]["title"],
            "genres": df.iloc[index]["genres"],
            "poster_url": poster_url,
            "similarity_score": round(
                float(similarity_scores[index]), 4
            )
        })

        if len(recommendations) == top_n:
            break

    if updated_posters:
        db.commit()
        
    return recommendations
