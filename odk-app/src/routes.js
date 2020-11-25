// Startpage
import BrowserStartPage from "./components/BrowserStartPage.vue";

// Login
import UserPage from "./components/authentication/UserPage.vue";
import CodePage from "./components/authentication/CodePage.vue";

// Onboarding
import WelcomePage from "./components/onboarding/WelcomePage.vue";
import TrialPage from "./components/onboarding/TrialPage.vue";
import RecommendationPage from "./components/onboarding/RecommendationPage.vue";
import ChecklistPage from "./components/onboarding/ChecklistPage.vue";
import NotifyClearStorage from "./components/onboarding/ClearStoragePage.vue";

// Manuals
import ManualInstall from "./components/manuals/ManualInstall.vue";
import ManualReset from "./components/manuals/ManualReset.vue";

// Stream
import StreamingClient from "./components/stream/StreamingClient.vue";


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
];
