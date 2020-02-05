// import Onboarding from './components/Onboarding.vue';
import StreamingClient from './components/StreamingClient';
// import DeviceLogin from './components/DeviceLogin.vue';
import BrowserStartPage from './components/BrowserStartPage.vue';
import PwaStartPage from './components/PwaStartPage.vue';
import RecommendationPage from './components/RecommendationPage.vue';
import ChecklistPage from './components/ChecklistPage.vue';


export const routes = [
    // {
    //     path: '/index.html',
    //     name : 'onboarding',
    //     component: Onboarding,
    //     alias: '/'
    // },
    {
        path: '/client',
        name : 'streaming-client',
        component: StreamingClient
    },
    // {
    //     path: '/login',
    //     name: 'login',
    //     component: DeviceLogin
    // },
    {
        path: '/browser',
        name: 'browser-startpage',
        component: BrowserStartPage
    },
    {
        path: '/pwa',
        name: 'pwa-startpage',
        component: PwaStartPage
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


]