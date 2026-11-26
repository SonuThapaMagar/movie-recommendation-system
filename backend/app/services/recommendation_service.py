import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.movie import Movie
from app.models.movie_tag import MovieTag
from app.models.rating import Rating
from app.services.movie_service import get_movie_details
from app.recommender.recommendation import (recommend_movies_from_ratings)

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
        
        if not movie:
            continue
        
        if (
            not movie.poster_url
            or not movie.overview
            or movie.rating is None
            or not movie.release_date
        ):
            details = get_movie_details(movie.title)

            if details:
                # Update only fields with valid values
                for field in [
                    "poster_url",
                    "overview",
                    "rating",
                    "release_date",
                    "tmdb_id"
                ]:
                    value = details.get(field)

                    if value is not None:
                        setattr(movie, field, value)
                        updated_movies = True
                
        recommendations.append({
            "movie_id": movie.movie_id,
            "title": movie.title,
            "genres":  movie.genres or "",
            "poster_url": movie.poster_url,
            "rating": movie.rating,
            "overview": movie.overview,
            "release_date": movie.release_date,
            "similarity_score": round(
                float(similarity_scores[index]), 4
            )
        })

        if len(recommendations) == top_n:
            break

    if updated_posters:
        db.commit()
        
    return recommendations

def get_recommendation_for_user(db:Session,user_id:int,top_n:int=10):
    #fetch logged in user ratings
    ratings = (
        db.query(Rating)
        .filter(Rating.user_id == user_id)
        .all()
    )

    
    #convert rating into dict
    user_ratings={
        rating.movie_id:rating.rating
        for rating in ratings
    }
    
    if not user_ratings:

        # Get popular movies using all available ratings
        popular_movies = (
            db.query(
                Movie,
                func.avg(Rating.rating).label("average_rating"),
                func.count(Rating.rating).label("rating_count")
            )
            .join(Rating, Movie.movie_id == Rating.movie_id)
            .group_by(Movie.movie_id)
            .having(func.count(Rating.rating) >= 5)
            .order_by(
                func.count(Rating.rating).desc(),
                func.avg(Rating.rating).desc()
            )
            .limit(top_n)
            .all()
        )

        results = []

        for movie, average_rating, rating_count in popular_movies:

            results.append({
                "movie_id": movie.movie_id,
                "title": movie.title,
                "genres": movie.genres,
                "poster_url": movie.poster_url,
                "overview": movie.overview,
                "rating": movie.rating,
                "release_date": movie.release_date,
                "predicted_rating": round(float(average_rating), 2)
            })

        return results
    
    
    #generate recommendation
    recommendations=recommend_movies_from_ratings(
        user_ratings=user_ratings,
        top_n=top_n
    )
    
    #extract recommended movie ID
    movie_ids=[movie_id for movie_id,predicted_rating in recommendations]
    
    if not movie_ids:
        return []
    
    movies=(
        db.query(Movie).filter(Rating.movie_id.in_(movie_ids)).all()
    )
    
    movies_by_id={movie.movie_id:movie for movie in movies}
    
    results=[]
    
    for movie_id,predicted_rating in recommendations:
        movie=movies_by_id.get(movie_id)
        
        if not movie: 
            continue
        
        results.append({
            "movie_id": movie.movie_id,
            "title": movie.title,
            "genres": movie.genres,
            "poster_url": movie.poster_url,
            "overview": movie.overview,
            "rating": movie.rating,
            "release_date": movie.release_date,
            "predicted_rating": round(
                float(predicted_rating), 2
            )
        })
    
    return results