import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import pickle
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parents[2]

DATA_PATH=BASE_DIR/"data"/"recommendation"/"recommendation_data.pkl"

with open(DATA_PATH,"rb")as file:
    recommendation_data=pickle.load(file)#restores our saved Python objects.
    
# Extract individual dataframes
user_item_matrix = recommendation_data["user_item_matrix"]
item_similarity_df = recommendation_data["item_similarity_df"]
all_movies = recommendation_data["all_movies"]

def recommend_movies_item_based(user_id,top_n=10):
    #get movies rated by the user
    user_ratings=user_item_matrix.loc[user_id].dropna()
    
    #find movies the user liked
    liked_movies=user_ratings[user_ratings>=4]
    
    recommendations={}
    
    #find similar movies for each liked movies
    for movie_id,rating in liked_movies.items():
        similar_movies=(
            item_similarity_df[movie_id]
            .sort_values(ascending=False)
            .drop(movie_id)
            .head(20)
        )
        
        for similar_movie_id,similarity_score in similar_movies.items():
            #skip movies already rated
            if similar_movie_id in user_ratings.index:
                continue
            
            if similarity_score<=0:
                continue
            
            if similar_movie_id not in recommendations:
                recommendations[similar_movie_id]=[0,0]
            
            recommendations[similar_movie_id][0]+=similarity_score*rating
            recommendations[similar_movie_id][1]+=similarity_score
            
    #calculated predicted scores
    predicted_ratings={}
    
    for movie_id,values in recommendations.items():
        predicted_ratings[movie_id]=values[0]/values[1]
        
    #sort recommendations by predicted score
    sorted_recommendations=sorted(
        predicted_ratings.items(),
        key=lambda x:x[1],
        reverse=True
    )
    
    return sorted_recommendations[:top_n]

def get_recommended_movies(user_id,top_n=10): 
    #Gets recommended movie IDs and scores
    recommendations=recommend_movies_item_based(user_id,top_n)
    
    #convert recommendations into DF
    recommendations_df=pd.DataFrame(
        recommendations,
        columns=["movie_id","predicted_rating"]
    )
    
    #Attach movie title and genres
    recommendations_df=recommendations_df.merge( #joins movie IDS with title and genres
        all_movies,
        on="movie_id",
        how="left"
    )
    
    return recommendations_df.to_dict(orient="records")

def recommend_movies_from_ratings(user_ratings,top_n=10):
    liked_movies={
        movie_id:rating
        for movie_id,rating in user_ratings.items()
        if rating>=4
    }
    
    if not liked_movies:
        return []
    
    recommendations={}
    
    #find similar movie for every liked movies
    for movie_id,rating in liked_movies.items():
        if movie_id not in item_similarity_df.columns:
            continue
        
        similar_movies=(
            item_similarity_df[movie_id]
            .sort_values(ascending=False)
            .drop(movie_id,errors="ignore")
            .head(10)
        )
        
        #calculate recommendation score
        for similar_movie_id,similarity_score in similar_movies.items():
            if similar_movie_id in user_ratings:
                continue
            
            if similarity_score<=0:
                continue
            
            if similar_movie_id not in recommendations:
                recommendations[similar_movie_id]=[0,0]
                
            recommendations[similar_movie_id][0]+=(
                similarity_score*rating
            )
            
            recommendations[similar_movie_id][1]+=similarity_score
            
        # Calculate weighted predicted ratings
        predicted_ratings = {}

        for movie_id, values in recommendations.items():

            predicted_ratings[movie_id] = (
                values[0] / values[1]
            )

        # Sort recommendations by predicted rating
        sorted_recommendations = sorted(
            predicted_ratings.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Return the top N recommendations
        return sorted_recommendations[:top_n]
