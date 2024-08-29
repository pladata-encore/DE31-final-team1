import {
  HomeIcon,
  UserCircleIcon,
  TableCellsIcon,
  InformationCircleIcon,
  ServerStackIcon,
  RectangleStackIcon,
} from "@heroicons/react/24/solid";
import { Home, Profile, Integrations, Notifications, Rules, Groups, Boards } from "@/pages/dashboard";
import { SignIn, SignUp } from "@/pages/auth";

const icon = {
  className: "w-5 h-5 text-inherit",
};

export const routes = [
  {
    layout: "dashboard",
    pages: [
      {
        icon: <HomeIcon {...icon} />,
        name: "홈",
        path: "/home",
        element: <Home />,
      },
      {
        icon: <TableCellsIcon {...icon} />,
        name: "데이터 통합",
        path: "/integrations",
        element: <Integrations />,
      },
      {
        icon: <TableCellsIcon {...icon} />,
        name: "데이터 그룹",
        path: "/Groups",
        element: <Groups />,
      },
      {
        icon: <TableCellsIcon {...icon} />,
        name: "룰셋",
        path: "/rules",
        element: <Rules />,
      },
      {
        icon: <TableCellsIcon {...icon} />,
        name: "대시보드",
        path: "/boards",
        element: <Boards />,
      },
      {
        icon: <InformationCircleIcon {...icon} />,
        name: "알림",
        path: "/notifications",
        element: <Notifications />,
      },
    ],
  },
  {
    title: "auth pages",
    layout: "auth",
    isAuth: false,
    pages: [
      {
        icon: <ServerStackIcon {...icon} />,
        name: "sign in",
        path: "/sign-in",
        element: <SignIn />,
      },
      {
        icon: <RectangleStackIcon {...icon} />,
        name: "sign up",
        path: "/sign-up",
        element: <SignUp />,
      },
    ],
  },
  {
    title: "user pages",
    layout: "dashboard",
    isAuth: true,
    pages: [
      {
        icon: <UserCircleIcon {...icon} />,
        name: "유저 정보",
        path: "/profile",
        element: <Profile />,
      },
    ],
  },
];

export default routes;
