import type { RecommendationResponse } from "@/types/movie";
import { api } from "@/api/api";

export const recommendationService = {
  getMovieRecommendations: (movieId: number, topN: number = 10) =>
    api.get<RecommendationResponse>(
      `/api/movies/${movieId}/recommendations?top_n=${topN}`,
    ),
};
