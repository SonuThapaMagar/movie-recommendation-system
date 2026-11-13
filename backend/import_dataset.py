
import pandas as pd
from pathlib import Path

from app.database.database import SessionLocal
from app.models.movie import Movie
from app.models.rating import Rating
from app.models.movie_tag import MovieTag


# Dataset directory
DATA_DIR = Path(__file__).resolve().parent / "data"


def import_movies(db):

    movies_df = pd.read_csv(DATA_DIR / "movies.csv")

    records = []

    for _, row in movies_df.iterrows():

        records.append({
            "movie_id": int(row["movieId"]),
            "title": row["title"],
            "genres": (
                "" if pd.isna(row["genres"])
                else row["genres"]
            )
        })

    db.bulk_insert_mappings(Movie, records)

    print(f"Imported {len(records)} movies")


def import_ratings(db):

    file_path = DATA_DIR / "ratings.csv"

    if not file_path.exists():
        print("ratings.csv not found. Skipping.")
        return

    total = 0

    # Read large datasets in batches
    for chunk in pd.read_csv(file_path, chunksize=10000):

        records = []

        for _, row in chunk.iterrows():

            records.append({
                "dataset_user_id": int(row["userId"]),
                "movie_id": int(row["movieId"]),
                "rating": float(row["rating"]),
                "timestamp": (
                    int(row["timestamp"])
                    if pd.notna(row["timestamp"])
                    else None
                )
            })

        db.bulk_insert_mappings(Rating, records)

        total += len(records)

    print(f"Imported {total} ratings")


def import_tags(db):

    file_path = DATA_DIR / "tags.csv"

    if not file_path.exists():
        print("tags.csv not found. Skipping.")
        return

    total = 0

    for chunk in pd.read_csv(file_path, chunksize=10000):

        records = []

        for _, row in chunk.iterrows():

            if pd.isna(row["tag"]):
                continue

            records.append({
                "dataset_user_id": int(row["userId"]),
                "movie_id": int(row["movieId"]),
                "tag": str(row["tag"]),
                "timestamp": (
                    int(row["timestamp"])
                    if pd.notna(row["timestamp"])
                    else None
                )
            })

        if records:
            db.bulk_insert_mappings(MovieTag, records)

        total += len(records)

    print(f"Imported {total} tags")


def main():

    db = SessionLocal()

    try:

        # Prevent accidental duplicate imports
        if db.query(Movie).first():
            print("Movies already exist. Import skipped.")
            return

        import_movies(db)

        # Commit movies first because ratings and tags
        # reference the movies table.
        db.commit()

        import_ratings(db)
        import_tags(db)

        db.commit()

        print("Dataset imported successfully!")

    except Exception as error:

        db.rollback()
        print("Import failed:", error)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
