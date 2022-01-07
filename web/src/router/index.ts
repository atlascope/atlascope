import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import Home from '../views/Home.vue';
import InvestigationsList from '../views/InvestigationsList.vue';
import InvestigationDetail from '../views/InvestigationDetail.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    component: Home,
  },
  {
    path: '/investigations',
    name: 'investigationsList',
    component: InvestigationsList,
  },
  {
    path: '/investigations/:investigation',
    name: 'investigationDetail',
    component: InvestigationDetail,
    props: true,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
