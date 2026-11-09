import type { Movie } from "@/types/movie";

interface MovieCardProps {
  movie: Movie;
}

const MovieCard = ({ movie }: MovieCardProps) => {
  // Convert the genre string into an array
  const genres = movie.genres
    .split("|")
    .filter((genre) => genre !== "(no genres listed)");
  return (
    <>
      <article className="overflow-hidden rounded-lg border border-[#D5D9DE] bg-white shadow-sm transition-shadow hover:shadow-md cursor-pointer">
        {/* Movie placeholder */}
        <div className="flex aspect-[3/4] items-center justify-center bg-[#E0EDF7]">
          <span className="text-4xl font-bold text-primary">
            {movie.title.charAt(0)}
          </span>
        </div>

        {/* Movie information */}
        <div className="p-3">
          <h3 className="line-clamp-2 text-sm font-semibold text-[#242A30]">
            {movie.title}
          </h3>

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
    </>
  );
};

export default MovieCard;
