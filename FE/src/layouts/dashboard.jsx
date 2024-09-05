import { Routes, Route } from "react-router-dom";
import { Cog6ToothIcon } from "@heroicons/react/24/solid";
import { IconButton, Typography } from "@material-tailwind/react";
import {
  Sidenav,
  DashboardNavbar,
  Configurator,
  Footer,
} from "@/widgets/layout";
import routes from "@/routes";
import { useMaterialTailwindController, setOpenConfigurator } from "@/context";
import { useEffect } from "react";

export function Dashboard() {
  const [controller, dispatch] = useMaterialTailwindController();
  const { sidenavType } = controller;
  const cookies = document.cookie.split(";").reduce((acc, cookie) => {
    const [key, value] = cookie.split("=").map(part => part.trim());
    acc[key] = value;
    return acc;
  }, {});

  function checkAuth(){
    if(!cookies.userAuth){
      setTimeout(() => {
        document.getElementById("req_login_modal").classList.remove("hidden");
      }, 500);
      setTimeout(() => {
        window.location.href = "/auth/sign-in";
      }, 4000);
    }
  }

  useEffect(() => {
    checkAuth();
  }, []);

  return (
    <div className="min-h-screen bg-blue-gray-50/50">
        {/* modal for req_login modal, covering full page(always on top) */}
      <div className="fixed bg-black bg-opacity-50 hidden w-full h-full z-50" id="req_login_modal" style={{zIndex: 1000}}>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-8 rounded-xl">
          <Typography variant="h6" color="blue-gray" className="font-bold">Please login to access this page</Typography>
          <Typography variant="h6" color="blue-gray" className="font-bold">Will redirect to login page in 3 seconds</Typography>
        </div>
      </div>
      <Sidenav
        routes={routes}
        brandImg={
          sidenavType === "dark" ? "/img/logo-ct.png" : "/img/logo-ct-dark.png"
        }
      />
      <div className="p-4 xl:ml-80">
        <DashboardNavbar />
        <Configurator />
        <IconButton
          size="lg"
          color="white"
          className="fixed bottom-8 right-8 z-40 rounded-full shadow-blue-gray-900/10"
          ripple={false}
          onClick={() => setOpenConfigurator(dispatch, true)}
        >
          <Cog6ToothIcon className="h-5 w-5" />
        </IconButton>
        <Routes>
          {routes.map(
            ({ layout, pages }) =>
              layout === "dashboard" &&
              pages.map(({ path, element }) => (
                <Route exact path={path} element={element} />
              ))
          )}
        </Routes>
        <div className="text-blue-gray-600">
          <Footer />
        </div>
      </div>
    </div>
  );
}

Dashboard.displayName = "/src/layout/dashboard.jsx";

export default Dashboard;
