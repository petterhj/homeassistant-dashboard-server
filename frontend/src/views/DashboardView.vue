<script setup>
import { format } from 'date-fns';
import { useI18n } from 'vue-i18n';
import { useServer } from '@/stores/server';

import ComponentLoader from '../components/ComponentLoader.vue';
import ErrorState from '../components/ErrorState.vue';

const { t } = useI18n();
const { error, getConfig } = useServer();

const config = await getConfig();
</script>

<template>
  <main class="h-full">
    <div
      v-if="!error && config?.dashboard?.components?.length"
      class="h-full grid grid-cols-3 gap-12 p-4 pb-14"
    >
      <ComponentLoader
        v-for="(component, index) in config.dashboard.components"
        :key="index"
        :type="component.type"
        :config="component"
      />
    </div>

    <ErrorState v-else :title="t('general.dashboardError')" :error="error" />
  </main>

  <div class="fixed bottom-5 left-5 text-sm">
    <span class="mdi mdi-refresh text-gray-300 mr-2" />
    <span class="text-gray-400 font-medium">
      {{ format(new Date(), 'dd.MM.yy - HH:mm') }}
    </span>
  </div>
</template>
