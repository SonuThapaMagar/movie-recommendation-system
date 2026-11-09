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
