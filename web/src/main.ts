import axios from 'axios';
import * as Sentry from '@sentry/vue';
import Vue from 'vue';
import VueCompositionAPI from '@vue/composition-api';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';

Vue.use(VueCompositionAPI);

const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_API_ROOT,
});

Sentry.init({
  Vue,
  dsn: process.env.VUE_APP_SENTRY_DSN,
});

store.dispatch.storeAxiosInstance(axiosInstance);
new Vue({
  provide: {
    axios: axiosInstance,
  },
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
