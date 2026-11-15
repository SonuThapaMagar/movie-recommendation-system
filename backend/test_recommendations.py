
from app.database.database import SessionLocal

from app.services.recommendation_service import (
    get_movie_recommendations
)


db = SessionLocal()

try:
    # MovieLens movie ID for Toy Story (1995) is commonly 1
    movie_id = 1

    recommendations = get_movie_recommendations(
        db=db,
        movie_id=movie_id,
        top_n=10
    )

    if recommendations is None:
        print("Movie not found")

    else:
        print("Recommendations:")

        for movie in recommendations:
            print(
                movie["title"],
                "| Similarity:",
                movie["similarity_score"]
            )

finally:
    db.close()
