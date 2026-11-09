import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { movieServices } from "@/services/movieService";
import type { Movie } from "@/types/movie";
import { ArrowLeft, Star } from "lucide-react";

const MovieDetails = () => {
  // Get movie ID from URL
  const { movieId } = useParams();

  // Store movie details
  const [movie, setMovie] = useState<Movie | null>(null);

  // Loading and error states
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        setIsLoading(true);
        setError(null);

        if (!movieId) {
          throw new Error("Invalid movie ID");
        }

        const response = await movieServices.getMovieById(Number(movieId));

        setMovie(response.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load movie");
      } finally {
        setIsLoading(false);
      }
    };

    fetchMovie();
  }, [movieId]);

  if (isLoading) {
    return (
      <div className="px-4 py-20 text-center text-[#64717C]">
        Loading movie details...
      </div>
    );
  }

  if (error || !movie) {
    return (
      <div className="px-4 py-20 text-center">
        <p className="text-red-600">{error || "Movie not found"}</p>

        <Link
          to="/"
          className="mt-4 inline-block text-brand-link hover:text-brand-highlight"
        >
          Back to Home
        </Link>
      </div>
    );
  }

  // Prepare genres
  const genres = movie.genres
    .split("|")
    .filter((genre) => genre !== "(no genres listed)");

  return (
    <div className="min-h-screen bg-background">
      {/* Movie backdrop */}
      <section className="relative overflow-hidden bg-[#173D58]">
        {/* Back navigation */}
        <div className="mx-auto max-w-7xl px-4 pt-8 sm:px-6 lg:px-8 ">
          <Link
            to="/"
            className="flex items-center gap-2 text-sm font-medium text-brand-link hover:text-brand-highlight"
          >
            <ArrowLeft size={16} /> Back to movies
          </Link>
        </div>

        {movie.poster_url && (
          <img
            src={movie.poster_url}
            alt=""
            className="absolute inset-0 h-full w-full object-cover opacity-20 blur-sm"
          />
        )}

        <div className="relative mx-auto flex max-w-7xl flex-col gap-8 px-4 py-10 sm:flex-row sm:items-center sm:px-6 lg:px-8 lg:py-16">
          {/* Movie poster */}
          <div className="mx-auto w-52 shrink-0 sm:mx-0 sm:w-64">
            {movie.poster_url ? (
              <img
                src={movie.poster_url}
                alt={`${movie.title} poster`}
                className="w-full rounded-lg shadow-xl"
              />
            ) : (
              <div className="flex aspect-[2/3] items-center justify-center rounded-lg bg-[#7EB2D6]">
                No Poster
              </div>
            )}
          </div>

          {/* Movie information */}
          <div className="text-white">
            <h1 className="text-2xl font-bold sm:text-4xl">{movie.title}</h1>

            {movie.release_date && (
              <p className="mt-3 text-sm text-white/75">
                Release Date: {movie.release_date}
              </p>
            )}

            {movie.rating != null && (
              <div className="right-2 top-2 flex items-center gap-1 rounded-md py-1.5 text-sm font-semibold textwhite backdrop-blur-sm">
                <Star size={16} className="fill-yellow-400 text-yellow-400" />

                <span>{movie.rating.toFixed(1)}</span>
              </div>
            )}
            {/* Genres */}
            <div className="mt-5 flex flex-wrap gap-2">
              {genres.map((genre) => (
                <span
                  key={genre}
                  className="rounded-full border border-white/40 px-3 py-1 text-xs"
                >
                  {genre}
                </span>
              ))}
            </div>

            {/* Overview */}
            <h2 className="mt-8 text-lg font-semibold">Overview</h2>

            <p className="mt-2 max-w-2xl text-sm leading-7 text-white/85">
              {movie.overview || "No overview available."}
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default MovieDetails;
