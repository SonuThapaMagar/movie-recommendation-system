import { api } from "@/api/api";

export const movieServices = {
  getMovies: (limit: number) =>
    api.get(`/api/movies/get_movies?limit=${limit}`),
};
