import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const MovieCard = () => {
  return (
    <>
      <Card className="border-border bg-card text-card-foreground transition-all hover:border-primary/50">
        {/* Movie title */}
        <CardHeader>
          <CardTitle>Interstellar</CardTitle>
          <CardDescription>Card Description</CardDescription>
          <CardAction>Card Action</CardAction>
        </CardHeader>

        {/* Movie information */}
        <CardContent>
          <p className="text-muted-foreground">Sci-Fi • Adventure • Drama</p>
          <button className="cursor-pointer mt-4 rounded-lg bg-primary px-4 py-2 text-primary-foreground hover:bg-primary/90">
            View Details
          </button>
        </CardContent>

        <CardFooter>
          <p>Card Footer</p>
        </CardFooter>
      </Card>
    </>
  );
};

export default MovieCard;
