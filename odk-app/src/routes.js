
import StreamingClient from './components/StreamingClient';
import BrowserStartPage from './components/BrowserStartPage.vue';
import PwaStartPage from './components/PwaStartPage.vue';
import RecommendationPage from './components/RecommendationPage.vue';
import ChecklistPage from './components/ChecklistPage.vue';


export const routes = [

    {
        path: '/client',
        name : 'streaming-client',
        component: StreamingClient
    },
    {
        path: '/',
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