import Vue from "vue";
import App from "./App.vue";
import { Button, Collapse, Switch } from "buefy";
import Vuelidate from "vuelidate";
import VueRouter from "vue-router";
import { routes } from "./routes";
import "./registerServiceWorker";
import VueAwesomeSwiper from "vue-awesome-swiper";
import "swiper/dist/css/swiper.css";
import VieOtpInput from "@bachdgvn/vue-otp-input";
import * as VueSpinnersCss from "vue-spinners-css";
import * as VueScrollTo from "vue-scrollto";

Vue.component("vie-otp-input", VieOtpInput);
export const eventBus = new Vue();

const router = new VueRouter({
  routes,
  mode: "history",
});

Vue.config.productionTip = false;
Vue.use(VueRouter);

// Buefy (Bulma) components:
Vue.use(Button);
Vue.use(Collapse);
Vue.use(Switch);

Vue.use(Vuelidate);
Vue.use(VueSpinnersCss);
Vue.use(VueScrollTo);
Vue.use(VueAwesomeSwiper, /* { default global options } */);

new Vue({
  router,
  render: h => h(App),
}).$mount("#app");
