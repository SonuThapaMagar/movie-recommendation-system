import type { Movie } from "@/types/movie";
import { Star } from "lucide-react";
import { Link } from "react-router-dom";

interface MovieCardProps {
  movie: Movie;
}

const MovieCard = ({ movie }: MovieCardProps) => {
  // Convert the genre string into an array
  const genres = movie.genres
    .split("|")
    .filter((genre) => genre !== "(no genres listed)");

  //Extract release year
  const releaseYear = movie.release_date
    ? movie.release_date.slice(0, 4)
    : null;

  return (
    <>
      <Link to={`/movies/${movie.movieId}`} className="block">
        <article className="overflow-hidden rounded-lg border border-[#D5D9DE] bg-white shadow-sm transition-shadow hover:shadow-md cursor-pointer">
          {/* Movie placeholder */}
          <div className="aspect-[3/4] overflow-hidden bg-[#E0EDF7]">
            {movie.poster_url ? (
              <img
                src={movie.poster_url}
                alt={`${movie.title} poster`}
                loading="lazy"
                className="h-full w-full object-cover transition-transform duration-300 hover:scale-105"
              />
            ) : (
              <div className="flex h-full items-center justify-center">
                <span className="text-4xl font-bold text-primary">
                  {movie.title.charAt(0)}
                </span>
              </div>
            )}
          </div>

          {/* Movie information */}
          <div className="p-3">
            <h3 className="line-clamp-2 text-sm font-semibold text-primary">
              {movie.title}
            </h3>

            {/* Movie rating badge */}
            {movie.rating != null && (
              <div className="right-2 top-2 flex items-center gap-1 rounded-md py-1.5 text-xs font-semibold text-[#242A30] backdrop-blur-sm">
                <Star size={16} className="fill-yellow-400 text-yellow-400" />

                <span>{movie.rating.toFixed(1)}</span>
              </div>
            )}

            {/* Release year */}
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
          </div>
        </article>
      </Link>
    </>
  );
};

export default MovieCard;
