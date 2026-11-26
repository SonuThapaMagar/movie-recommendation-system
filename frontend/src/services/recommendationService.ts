import type { RecommendationResponse } from "@/types/movie";
import { api } from "@/api/api";

export const recommendationService = {
  // Recommendations based on a particular movie
  getMovieRecommendations: (movieId: number, topN: number = 10) =>
    api.get<RecommendationResponse>(
      `/api/movies/${movieId}/recommendations?top_n=${topN}`,
    ),

  // Personalized recommendations for the logged-in user
  getPersonalizedRecommendations: () =>
    api.get<RecommendationResponse>("/api/recommendations/me"),
};
