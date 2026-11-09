import MovieCard from "@/components/custom/MovieCard";
import { movieServices } from "@/services/movieService";
import type { Movie } from "@/types/movie";
import { useEffect, useState } from "react";

const Home = () => {
  // Store movies received from the api
  const [movies, setMovies] = useState<Movie[]>([]);

  //Loading and error state
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch movies
  useEffect(() => {
    const fetchMovies = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const response = await movieServices.getMovies(20);
        setMovies(response.data.movies);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Something went wrong");
      } finally {
        setIsLoading(false);
      }
    };
    fetchMovies();
  }, []);

  return (
    <>
      <div className="w-full">
        {/* Hero section */}
        <section className="bg-white px-4 py-12 sm:py-16 lg:py-20">
          <div className="mx-auto max-w-7xl text-center">
            <h1 className="text-3xl font-bold text-[#242A30] sm:text-4xl lg:text-5xl">
              Discover Movies You'll Love
            </h1>

            <p className="mx-auto mt-4 max-w-2xl text-sm text-[#64717C] sm:text-base">
              Explore movies, discover new favorites, and get personalized
              recommendations based on your interests.
            </p>

            <div className="mt-8 flex justify-center">
              <button className="rounded-md bg-primary px-6 py-3 text-sm font-semibold text-primary-foreground transition-colors hover:bg-[#2180CB]">
                Explore Movies
              </button>
            </div>
          </div>
        </section>

        {/* Popular movies section */}
        <section className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
          <div className="mb-6">
            <h2 className="text-xl font-bold text-[#242A30] sm:text-2xl">
              Popular Movies
            </h2>

            <p className="mt-1 text-sm text-[#64717C]">
              Explore movies you might enjoy.
            </p>
          </div>

          {/* Loading state */}
          {isLoading && (
            <p className="text-sm text-[#64717C]">Loading movies...</p>
          )}

          {/* Error state */}
          {error && <p className="text-sm text-red-600">{error}</p>}

          {/* Movie cards  */}
          {!isLoading && !error && (
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
              {movies.map((movie) => (
                <MovieCard key={movie.movieId} movie={movie} />
              ))}
            </div>
          )}

          {/* Empty state */}
          {!isLoading && !error && movies.length === 0 && (
            <p className="text-sm text-[#64717C]">No movies found.</p>
          )}
        </section>
      </div>
    </>
  );
};

export default Home;
