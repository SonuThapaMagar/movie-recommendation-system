import { Link } from "react-router-dom";
import { Menu, X, Search } from "lucide-react";
import { useState } from "react";
import { cn } from "cn";

const HeaderLayout = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  return (
    <>
      <header className="w-full bg-primary text-primary-foreground shadow-sm">
        {/* Main navbar */}
        <nav className="mx-auto flex min-h-14 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          {/* Website logo */}
          <Link to="/" className="shrink-0 text-xl font-bold">
            WatchNext
          </Link>

          {/* Desktop navigation */}
          <div className="hidden items-center gap-6 md:flex">
            <Link to="/" className="transition-colors hover:text-white/70">
              Home
            </Link>

            <Link
              to="/movies"
              className="transition-colors hover:text-white/70"
            >
              Explore
            </Link>

            <Link
              to="/search"
              className="flex items-center gap-2 transition-colors hover:text-white/70"
            >
              <Search size={17} />
              Search
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            type="button"
            className="relative rounded-md p-2 transition-colors hover:bg-white/10 md:hidden cursor-pointer"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label={
              isMenuOpen ? "Close navigation menu" : "Open navigation menu"
            }
            aria-expanded={isMenuOpen}
          >
            <div className="relative h-6 w-6">
              <Menu
                className={cn(
                  "absolute inset-0 h-6 w-6 transition-all duration-700 ease-in-out",
                  isMenuOpen
                    ? "rotate-90 scale-0 opacity-0"
                    : "rotate-0 scale-100 opacity-100",
                )}
              />
              <X
                className={cn(
                  "absolute inset-0 h-6 w-6 transition-all duration-700 ease-in-out",
                  isMenuOpen
                    ? "rotate-0 scale-100 opacity-100"
                    : "-rotate-90 scale-0 opacity-0",
                )}
              />
            </div>
          </button>
        </nav>

        {/* Mobile navigation dropdown */}
        {isMenuOpen && (
          <div className="border-t border-white/20 px-4 py-3 md:hidden">
            <div className="flex flex-col gap-3">
              <Link
                to="/"
                onClick={() => setIsMenuOpen(false)}
                className="rounded-md px-3 py-2 hover:bg-white/10"
              >
                Home
              </Link>

              <Link
                to="/movies"
                onClick={() => setIsMenuOpen(false)}
                className="rounded-md px-3 py-2 hover:bg-white/10"
              >
                Explore
              </Link>

              <Link
                to="/search"
                onClick={() => setIsMenuOpen(false)}
                className="rounded-md px-3 py-2 hover:bg-white/10"
              >
                <span className="flex items-center gap-2">
                  <Search size={17} />
                  Search
                </span>
              </Link>
            </div>
          </div>
        )}
      </header>
    </>
  );
};

export default HeaderLayout;
