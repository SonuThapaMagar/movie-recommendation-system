import MovieCard from "@/components/custom/MovieCard";
import { movieServices } from "@/services/movieService";
import type { Movie } from "@/types/movie";
import { useEffect, useMemo, useState } from "react";

const Home = () => {
  // Store movies received from the api
  const [movies, setMovies] = useState<Movie[]>([]);

  //Loading and error state
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  //search
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedGenre, setSelectedGenre] = useState("All");

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

  // Extract unique genres from fetched movies
  const genres = useMemo(() => {
    const allGenres = movies.flatMap((movie) =>
      movie.genres.split("|").filter((genre) => genre !== "(no genres listed)"),
    );
    return ["All", ...new Set(allGenres)].sort((a, b) => {
      if (a === "All") return -1;
      if (b === "All") return 1;
      return a.localeCompare(b);
    });
  }, [movies]);

  // Filter movies based on search and selected genre
  const filteredMovies = useMemo(() => {
    return movies.filter((movie) => {
      const matchesSearch = movie.title
        .toLowerCase()
        .includes(searchQuery.toLowerCase().trim());

      const matchesGenre =
        selectedGenre === "All" ||
        movie.genres.split("|").includes(selectedGenre);

      return matchesSearch && matchesGenre;
    });
  }, [movies, searchQuery, selectedGenre]);

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

          {/* Search and genre filters */}
          <div className="mb-8 flex flex-col gap-3 sm:flex-row">
            {/* Search input */}
            <input
              type="search"
              placeholder="Search movies by title..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-md border border-[#D5D9DE] bg-white px-4 py-3 text-sm text-[#242A30] outline-none focus:border-primary sm:flex-1"
            />
          </div>

          {/* Genre dropdown */}
          <select
            value={selectedGenre}
            onChange={(e) => setSelectedGenre(e.target.value)}
            className="w-full rounded-md border border-[#D5D9DE] bg-white px-4 py-3 text-sm text-[#242A30] outline-none focus:border-primary sm:w-52"
          >
            {genres.map((genre) => (
              <option key={genre} value={genre}>
                {genre === "All" ? "All Genres" : genre}
              </option>
            ))}
          </select>
          {/* Loading state */}
          {isLoading && (
            <p className="text-sm text-[#64717C]">Loading movies...</p>
          )}

          {/* Error state */}
          {error && <p className="text-sm text-red-600">{error}</p>}

          {/* Movie cards  */}
          {!isLoading && !error && (
            <>
              <p>Showing{filteredMovies.length} movies</p>

              {filteredMovies.length > 0 ? (
                <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
                  {filteredMovies.map((movie) => (
                    <MovieCard key={movie.movieId} movie={movie} />
                  ))}
                </div>
              ) : (
                <div className="rounded-lg bg-white px-4 py-12 text-center">
                  <p className="font-medium text-[#242A30]">No movies found</p>
                  <p className="mt-2 text-sm text-[#64717C]">
                    Try another movie title or genre.
                  </p>
                </div>
              )}
            </>
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
