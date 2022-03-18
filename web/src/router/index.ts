import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import InvestigationsList from '../views/InvestigationsList.vue';
import InvestigationDetail from '../views/InvestigationDetail.vue';
import EmbeddingsDetail from '../views/EmbeddingsDetail.vue';

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
    path: '/investigations/:investigation/embeddings',
    name: 'embeddingsDetail',
    component: EmbeddingsDetail,
    props: true,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
