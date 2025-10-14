import { createRouter, createWebHistory } from 'vue-router';
import { useServer } from '@/stores/server';
import DashboardView from '../views/DashboardView.vue';
import ErrorView from '../views/ErrorView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      beforeEnter: (to, from, next) => {
        const { config } = useServer();
        const availableViews = config.value?.views || [];
        const firstView = availableViews.length > 0 ? availableViews[0] : null;
        
        if (firstView) {
          next({ name: 'view', params: { viewName: firstView.name } });
        } else {
          next({ 
            name: 'error',
            state: { messageKey: 'errors.noConfiguration' },
            replace: true,
          });
        }
      },
    },
    {
      path: '/:viewName([a-zA-Z0-9_-]+)',
      name: 'view',
      component: DashboardView,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'error',
      component: ErrorView,
    },
  ],
});

export default router;
