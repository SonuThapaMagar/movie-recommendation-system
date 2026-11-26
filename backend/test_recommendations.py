from app.database.database import SessionLocal
from app.services.recommendation_service import (
    get_movie_recommendations
)
from app.recommender.recommendation import recommend_movies_item_based,get_recommended_movies


db = SessionLocal()

# try:
#     # MovieLens movie ID for Toy Story (1995) is commonly 1
#     movie_id = 1

#     recommendations = get_movie_recommendations(
#         db=db,
#         movie_id=movie_id,
#         top_n=10
#     )

#     if recommendations is None:
#         print("Movie not found")

#     else:
#         print("Recommendations:")

#         for movie in recommendations:
#             print(
#                 movie["title"],
#                 "| Similarity:",
#                 movie["similarity_score"]
#             )
# finally:
#     db.close()


from app.recommender.recommendation import (
    user_item_matrix,
    item_similarity_df,
    all_movies
)
# print("User-item matrix:", user_item_matrix.shape)
# print("Item similarity matrix:", item_similarity_df.shape)
# print("Movies:", all_movies.shape)

# recommendations = recommend_movies_item_based(user_id=1, top_n=10)
# print(recommendations)


# recommendations = get_recommended_movies(user_id=1, top_n=10)

# for movie in recommendations:
#     print(
#         movie["title"],
#         "| Score:",
#         round(movie["similarity_score"], 2)
#     )
    
print(item_similarity_df.shape)

print(item_similarity_df.index[:10].tolist())

print(item_similarity_df.columns[:10].tolist())