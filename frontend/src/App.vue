<script setup>
import nb from 'date-fns/locale/nb';
import setDefaultOptions from 'date-fns/setDefaultOptions';
import { onMounted } from 'vue';
import { RouterView } from 'vue-router';
import { useServer } from '@/stores/server';
import i18n from './i18n';

const { getConfig } = useServer();

onMounted(async () => {
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
});
</script>

<template>
  <Suspense>
    <template #default>
      <RouterView />
    </template>

    <template #fallback>
      <LoadingState />
    </template>
  </Suspense>
</template>
