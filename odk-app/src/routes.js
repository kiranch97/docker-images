import BrowserStartPage from "./components/BrowserStartPage.vue";
import WelcomePage from "./components/WelcomePage.vue";
import RecommendationPage from "./components/RecommendationPage.vue";
import ChecklistPage from "./components/ChecklistPage.vue";
import UserPage from "./components/UserPage.vue";
import LoginPage from "./components/LoginPage";
import NotifyClearStorage from "./components/NotifyClearStorage";
import ManualInstall from "./components/manuals/ManualInstall";
import ManualReset from "./components/manuals/ManualReset";
import StreamingClient from "./components/StreamingClient";

export const routes = [
  {
    path: "/",
    name: "browser-startpage",
    component: BrowserStartPage,
    props: true,
  },
  {
    path: "/welcome",
    name: "welcome-page",
    component: WelcomePage,
  },
  {
    path: "/recommendation",
    name: "recommendation-page",
    component: RecommendationPage,
  },
  {
    path: "/checklist",
    name: "checklist-page",
    component: ChecklistPage,
  },
  {
    path: "/user",
    name: "user-page",
    component: UserPage,
  },
  {
    path: "/login",
    name: "login-page",
    component: LoginPage,
    props: true,
  },
  {
    path: "/client",
    name: "streaming-client",
    component: StreamingClient,
    props: true,
  },
  {
    path: "/clear-storage",
    name: "clear-storage",
    component: NotifyClearStorage,
    props: true,
  },
  {
    path: "/installation-manual",
    name: "installation-manual",
    component: ManualInstall,
    props: true,
  },
  {
    path: "/reset-manual",
    name: "reset-manual",
    component: ManualReset,
    props: true,
  },
];
