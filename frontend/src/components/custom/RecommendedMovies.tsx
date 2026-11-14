import { useEffect, useState } from "react";

import { recommendationService } from "@/services/recommendationService";
import type { RecommendedMovie } from "@/types/movie";

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
        {movies.map((movie) => (
          <div
            key={movie.movie_id}
            className="rounded-lg overflow-hidden border shadow-sm"
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

              <p className="text-sm text-gray-500 mt-2">{movie.genres}</p>

              <p className="text-sm font-medium mt-3">
                Similarity: {(movie.similarity_score * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default RecommendedMovies;
