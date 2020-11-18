import BrowserStartPage from "./components/BrowserStartPage.vue";
import WelcomePage from "./components/WelcomePage.vue";
import UserPage from "./components/UserPage.vue";
import CodePage from "./components/CodePage.vue";
import TrialPage from "./components/TrialPage.vue";
import RecommendationPage from "./components/RecommendationPage.vue";
import ChecklistPage from "./components/ChecklistPage.vue";
import StreamingClient from "./components/StreamingClient";
import NotifyClearStorage from "./components/NotifyClearStorage";
import ManualInstall from "./components/manuals/ManualInstall";
import ManualReset from "./components/manuals/ManualReset";
// import LoginPage from "./components/LoginPage";

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
    path: "/user",
    name: "user-page",
    component: UserPage,
  },
  {
    path: "/code",
    name: "code-page",
    component: CodePage,
    props: true,
  },
  {
    path: "/trial",
    name: "trial-page",
    component: TrialPage,
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
  // {
  //   path: "/login",
  //   name: "login-page",
  //   component: LoginPage,
  //   props: true,
  // },
];
