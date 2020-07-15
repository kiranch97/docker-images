import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import VueRouter from "vue-router";
import { routes } from "./routes";
import VueLodash from "vue-lodash";
import lodash from "lodash";
import moment from "vue-moment";
import { Button, Collapse, Switch } from "buefy";
import Vuelidate from "vuelidate";
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

// Utilities
Vue.use(VueLodash, { lodash: lodash });
Vue.use(moment);

// Buefy (Bulma) components.
Vue.use(Button);
Vue.use(Collapse);
Vue.use(Switch);

// Vue third-party components and directives.
Vue.use(Vuelidate);
Vue.use(VueSpinnersCss);
Vue.use(VueScrollTo);
Vue.use(VueAwesomeSwiper, /* { default global options } */);

// Global ODK components.
Vue.component("odk-container", () => import("@/components/elements/Container.vue"));

new Vue({
  router,
  render: h => h(App),
}).$mount("#app");
