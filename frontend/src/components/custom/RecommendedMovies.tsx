import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { recommendationService } from "@/services/recommendationService";
import type { RecommendedMovie } from "@/types/movie";
import { Star } from "lucide-react";

interface RecommendedMoviesProps {
  movieId: number;
}

const RecommendedMovies = ({ movieId }: RecommendedMoviesProps) => {
  const [movies, setMovies] = useState<RecommendedMovie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await recommendationService.getMovieRecommendations(
          movieId,
          10,
        );

        setMovies(response.data.recommendations);
      } catch (error) {
        console.error("Recommendation error:", error);
        setError("Unable to load recommendations.");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [movieId]);

  if (loading) {
    return <p>Loading recommendations...</p>;
  }

  if (error) {
    return <p className="text-red-500">{error}</p>;
  }

  if (movies.length === 0) {
    return <p>No recommendations available.</p>;
  }

  return (
    <section className="mt-8">
      <h2 className="text-2xl font-bold mb-5">Recommended Movies</h2>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5">
        {movies.map((movie) => {
          // Extract genres for this movie
          const genres = (movie.genres || "")
            .split(/\s+/)
            .filter(
              (genre) =>
                genre !== "(no" && genre !== "genres" && genre !== "listed)",
            );

          // Extract release year
          const releaseYear = movie.release_date
            ? movie.release_date.slice(0, 4)
            : null;

          return (
            <Link
              key={movie.movie_id}
              to={`/movies/${movie.movie_id}`}
              className="block rounded-lg overflow-hidden border shadow-sm hover:shadow-lg hover:scale-[1.02] transition-all duration-200"
            >
              {/* Movie Poster */}
              <div className="aspect-[2/3] bg-gray-200">
                <img
                  src={movie.poster_url || "/placeholder-movie.png"}
                  alt={movie.title}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Movie Information */}
              <div className="p-3">
                <h3 className="font-semibold line-clamp-2">{movie.title}</h3>

                {/* Movie rating */}
                {movie.rating != null && (
                  <div className="right-2 top-2 flex items-center gap-1 rounded-md py-1.5 text-xs font-semibold text-[#242A30] backdrop-blur-sm">
                    <Star
                      size={16}
                      className="fill-yellow-400 text-yellow-400"
                    />

                    <span>{movie.rating.toFixed(1)}</span>
                  </div>
                )}

                {/* Release Year */}
                {releaseYear && (
                  <p className="mt-1 text-xs text-[#64717C]">{releaseYear}</p>
                )}

                {/* Genres */}
                <div className="mt-2 flex flex-wrap gap-1">
                  {genres.slice(0, 2).map((genre) => (
                    <span
                      key={genre}
                      className="rounded bg-[#E0EDF7] px-2 py-1 text-xs text-[#00619D]"
                    >
                      {genre}
                    </span>
                  ))}
                </div>

                {/* <p className="text-sm font-medium mt-3">
                Similarity: {(movie.similarity_score * 100).toFixed(1)}%
              </p> */}
              </div>
            </Link>
          );
        })}
      </div>
    </section>
  );
};

export default RecommendedMovies;
