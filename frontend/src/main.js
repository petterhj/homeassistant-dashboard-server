import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import nb from 'date-fns/locale/nb';
import setDefaultOptions from 'date-fns/setDefaultOptions';
import { useDashboard } from '@/stores/dashboard';

import App from './App.vue';
import router from './router';
import messages from './config/i18n';

import './assets/main.css';

const { dashboard } = useDashboard();

const app = createApp(App);
const i18n = createI18n({
  legacy: false,
  locale: dashboard.value?.locale?.default || 'en',
  fallbackLocale: dashboard.value?.locale?.fallback || 'en',
  messages,
});

setDefaultOptions({
  locale: dashboard.value?.locale?.default === 'nb' ? nb : null,
});

app.use(router);
app.use(i18n);

app.mount('#app');
