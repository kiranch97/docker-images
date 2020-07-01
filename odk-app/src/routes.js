import BrowserStartPage from './components/BrowserStartPage.vue';
import WelcomePage from './components/WelcomePage.vue';
import RecommendationPage from './components/RecommendationPage.vue';
import ChecklistPage from './components/ChecklistPage.vue';
import UserPage from './components/UserPage.vue';
import StreamingClient from './components/StreamingClient';


export const routes = [
    {
        path: '/',
        name: 'browser-startpage',
        component: BrowserStartPage
    },
    {
        path: '/welcome',
        name: 'welcome-page',
        component: WelcomePage
    },
    {
        path: '/recommendation',
        name: 'recommendation-page',
        component: RecommendationPage
    },
    {
        path: '/checklist',
        name: 'checklist-page',
        component: ChecklistPage
    },
    {
        path: '/user',
        name: 'user-page',
        component: UserPage,
        props: true
    },
    {
        path: '/client',
        name: 'streaming-client',
        component: StreamingClient,
        props: true
    }
]