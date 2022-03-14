import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import InvestigationsList from '../views/InvestigationsList.vue';
import InvestigationDetail from '../views/InvestigationDetail.vue';
import MapProjection from '../views/MapProjection.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    name: 'investigationsList',
    component: InvestigationsList,
  },
  {
    path: '/investigations/:investigation',
    name: 'investigationDetail',
    component: InvestigationDetail,
    props: true,
  },
  {
    path: '/demo',
    name: 'mapProjection',
    component: MapProjection,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
