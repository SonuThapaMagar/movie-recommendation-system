import MainLayout from "@/layout/MainLayout";
import Home from "@/pages/dashboard/Home";
import MovieDetails from "@/pages/dashboard/MovieDetails";
import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([
  {
    element: <MainLayout />,
    children: [
      { path: "/", element: <Home /> },
      {
        path: "/movies/:movieId",
        element: <MovieDetails />,
      },
    ],
  },
]);
