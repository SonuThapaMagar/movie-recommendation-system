import HeaderLayout from "./HeaderLayout";
import FooterLayout from "./FooterLayout";
import { Outlet } from "react-router-dom";

function MainLayout() {
  return (
    <div className="flex min-h-screen flex-col overflow-x-hidden bg-background text-foreground">
      {/* Website header */}
      <HeaderLayout />

      {/* Page content */}
      <main className="w-full flex-1">
        <Outlet />
      </main>

      {/* Website footer */}
      <FooterLayout />
    </div>
  );
}

export default MainLayout;
