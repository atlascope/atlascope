import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import InvestigationsList from '../views/InvestigationsList.vue';
import InvestigationDetail from '../views/InvestigationDetail.vue';
import VtkViewer from '../views/VtkViewer.vue';

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
    path: '/vtkviewer',
    name: 'vtkViewer',
    component: VtkViewer,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
