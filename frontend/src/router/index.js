import { createRouter, createWebHistory } from "vue-router";
import ApplicationListView from "../views/ApplicationListView.vue";
import NewApplicationView from "../views/NewApplicationView.vue";
import ReviewResultView from "../views/ReviewResultView.vue";

const routes = [
  { path: "/", name: "list", component: ApplicationListView },
  { path: "/applications/new", name: "new", component: NewApplicationView },
  { path: "/review", name: "review", component: ReviewResultView }
];

export default createRouter({
  history: createWebHistory(),
  routes
});

