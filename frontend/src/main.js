import nb from 'date-fns/locale/nb';
import setDefaultOptions from 'date-fns/setDefaultOptions';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import i18n from './i18n';
import { useServer } from './stores/server';

import './assets/main.css';

async function initializeApp() {
  const { getConfig } = useServer();
  
  try {
    console.log('Loading configuration...');
    const config = await getConfig();
    
    if (config) {
      if (config?.locale?.default) {
        console.log(`Setting locale to: ${config.locale.default}`);
        i18n.global.locale.value = config.locale.default;
        setDefaultOptions({
          locale: config.locale.default === 'nb' ? nb : null,
        });
      }
      if (config?.locale?.fallback) {
        i18n.global.fallbackLocale.value = config.locale.fallback;
      }
    }
    
    console.log('Configuration loaded successfully!');
  } catch (error) {
    console.error('Failed to load configuration:', error);
    throw error;
  }
}

async function startApp() {
  try {
    await initializeApp();
  } catch (error) {
    console.error('Failed to start application:', error);
  } finally {
    const app = createApp(App);
    app.use(router);
    app.use(i18n);
    app.mount('#app');
  }
}

// Start the application
startApp();
