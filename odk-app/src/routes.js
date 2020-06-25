import BrowserStartPage from './components/BrowserStartPage.vue';
import RecommendationPage from './components/RecommendationPage.vue';
import ChecklistPage from './components/ChecklistPage.vue';
import UserPage from './components/UserPage.vue';
import LoginPage from './components/LoginPage';
import ChromeManualPage from './components/manuals/ChromeManualPage';
import EdgeManualPage from './components/manuals/EdgeManualPage';
import FirefoxManualPage from './components/manuals/FirefoxManualPage';
import IosManualPage from './components/manuals/IosManualPage';
import DesktopManualPage from './components/manuals/DesktopManualPage';
import OtherBrowsersManualPage from './components/manuals/OtherBrowsersManualPage';
import StreamingClient from './components/StreamingClient';


export const routes = [
    {
        path: '/',
        name: 'browser-startpage',
        component: BrowserStartPage,
        props: true
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
        component: UserPage
    },
    {
        path: '/login',
        name: 'login-page',
        component: LoginPage
    },
    {
        path: '/client',
        name: 'streaming-client',
        component: StreamingClient
    },
    {
        path: '/chrome-manual',
        name: 'chrome-manual-page',
        component: ChromeManualPage,
        props: true
    },
    {
        path: '/edge-manual',
        name: 'edge-manual-page',
        component: EdgeManualPage,
        props: true
    },
    {
        path: '/firefox-manual',
        name: 'firefox-manual-page',
        component: FirefoxManualPage,
        props: true
    },
    {
        path: '/ios-manual',
        name: 'Iosio-manual-page',
        component: IosManualPage,
        props: true
    },
    {
        path: '/desktop-manual',
        name: 'desktop-manual-page',
        component: DesktopManualPage,
        props: true
    },
    {
        path: '/other-browsers-manual',
        name: 'other-browsers-manual-page',
        component: OtherBrowsersManualPage,
        props: true
    },
]