import { createApp } from 'vue';
import { createI18n } from 'vue-i18n';
import nb from 'date-fns/locale/nb';
import setDefaultOptions from 'date-fns/setDefaultOptions';

import App from './App.vue';
import router from './router';
import messages from './config/i18n';

import './assets/main.css';

const app = createApp(App);
const i18n = createI18n({
  legacy: false,
  locale: import.meta.env.VITE_LOCALE,
  fallbackLocale: 'en',
  messages,
});

setDefaultOptions({
  locale: import.meta.env.VITE_LOCALE === 'nb' ? nb : null,
});

app.use(router);
app.use(i18n);

app.mount('#app');
