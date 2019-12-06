import Onboarding from './components/Onboarding.vue';
import StreamingClient from './components/StreamingClient';
import DeviceLogin from './components/DeviceLogin.vue';


export const routes = [
    {
        path: '/index.html',
        name : 'onboarding',
        component: Onboarding,
        alias: '/'
    },
    {
        path: '/client',
        name : 'streaming-client',
        component: StreamingClient
    },
    {
        path: '/login',
        name: 'login',
        component: DeviceLogin
    },


]