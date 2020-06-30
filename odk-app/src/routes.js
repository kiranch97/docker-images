import BrowserStartPage from "./components/BrowserStartPage.vue";
import RecommendationPage from "./components/RecommendationPage.vue";
import ChecklistPage from "./components/ChecklistPage.vue";
import UserPage from "./components/UserPage.vue";
import LoginPage from "./components/LoginPage";
import InstallManual from "./components/manuals/InstallManual";
import StreamingClient from "./components/StreamingClient";

export const routes = [
  {
    path: "/",
    name: "browser-startpage",
    component: BrowserStartPage,
    props: true,
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
  },
  {
    path: "/client",
    name: "streaming-client",
    component: StreamingClient,
  },
  {
    path: "/installation-manual",
    name: "installation-manual",
    component: InstallManual,
    props: true,
  },
];
