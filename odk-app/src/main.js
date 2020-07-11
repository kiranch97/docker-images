import Vue from "vue";
import App from "./App.vue";
import Buefy from "buefy";
import Vuelidate from "vuelidate";
import VueRouter from "vue-router";
import moment from "vue-moment";
import { routes } from "./routes";
import "./registerServiceWorker";
import "buefy/dist/buefy.css";
import VueAwesomeSwiper from "vue-awesome-swiper";
import "swiper/dist/css/swiper.css";
import VieOtpInput from "@bachdgvn/vue-otp-input";
import * as VueSpinnersCss from "vue-spinners-css";
import * as VueScrollTo from "vue-scrollto";

Vue.use(VueScrollTo);

// import { makeServer } from './server'

// if (process.env.NODE_ENV == "development") {
//   console.log("I am in development mode")
//   makeServer()
// }

Vue.component("vie-otp-input", VieOtpInput);
export const eventBus = new Vue();

// document.cookie = 'cross-site-cookie=bar; SameSite=None';

const router = new VueRouter({
  routes,
  mode: "history",
});

Vue.config.productionTip = false;
Vue.use(VueSpinnersCss);
Vue.use(Vuelidate);
Vue.use(Buefy);
Vue.use(VueRouter);
Vue.use(moment);
Vue.use(VueAwesomeSwiper, /* { default global options } */);

new Vue({
  router,
  render: h => h(App),
}).$mount("#app");
