export interface Movie {
  movieId: number;
  title: string;
  genres: string;
  poster_url: string | null;

  tmdb_id?: number | null;
  rating?: number | null;
  overview?: string | null;
  release_date?: string | null;
}

export interface MovieResponse {
  count: number;
  movies: Movie[];
}

export interface RecommendedMovie {
  movie_id: number;
  title: string;
  genres: string;
  poster_url: string | null;
  similarity_score: number;
}

export interface RecommendationResponse {
  movie_id: number;
  count: number;
  recommendations: RecommendedMovie[];
}
