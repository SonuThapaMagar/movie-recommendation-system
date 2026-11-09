import { api } from "@/api/api";
import type { Movie, MovieResponse } from "@/types/movie";

export const movieServices = {
  getMovies: (limit: number) =>
    api.get<MovieResponse>(`/api/movies/get_movies?limit=${limit}`),

  getMovieById: (movieId: number) => api.get<Movie>(`/api/movies/${movieId}`),
};
