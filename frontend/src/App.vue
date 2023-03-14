<script setup>
import nb from 'date-fns/locale/nb';
import setDefaultOptions from 'date-fns/setDefaultOptions';
import { ref, onBeforeMount } from 'vue';
import { useI18n } from 'vue-i18n';
import { RouterView } from 'vue-router';
import { useServer } from '@/stores/server';
import i18n from './i18n';

import ErrorState from '@/components/ErrorState.vue';

const { t } = useI18n();
const { getConfig } = useServer();

const error = ref(null);

onBeforeMount(async () => {
  try {
    const config = await getConfig();
    if (config) {
      if (config?.locale?.default) {
        i18n.global.locale.value = config.locale.default;
        setDefaultOptions({
          locale: config.locale.default === 'nb' ? nb : null,
        });
      }
      if (config?.locale?.fallback) {
        i18n.global.fallbackLocale.value = config.locale.fallback;
      }
    }
  } catch (err) {
    console.error('Error while reading config:', err.message);
    console.debug(err);
    error.value = err;
  }
});
</script>

<template>
  <RouterView v-if="!error" />
  <ErrorState
    v-else
    :title="t('general.dashboardError')"
    :error="error"
    icon="view-dashboard-outline"
    size="large"
  />
</template>
