import { createRouter, createWebHistory } from 'vue-router';
import DashboardView from '../views/DashboardView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/error',
      name: 'error',
      component: () => import('../views/ErrorView.vue'),
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  try {
    const response = await fetch('/ha/');

    if (!response?.ok) {
      response.json().then((json) => {
        console.error(json.detail);
      });
      if (to.name !== 'error') {
        next({ name: 'error' });
      } else {
        next();
      }
    } else {
      if (to.name === 'error') {
        next({ name: 'dashboard' });
      } else {
        next();
      }
    }
  } catch (error) {
    console.log('Fetch error: ', error);
    if (to.name !== 'error') {
      next({ name: 'error' });
    }
  }
});

export default router;
