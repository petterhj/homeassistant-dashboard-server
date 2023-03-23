<script setup>
import { format } from 'date-fns';
import { useServer } from '@/stores/server';

import ComponentLoader from '../components/ComponentLoader.vue';

const { config } = useServer();
</script>

<template>
  <main class="h-full">
    <div
      v-if="config?.dashboard?.components?.length"
      class="h-full grid grid-cols-3 gap-12 p-4 pb-14"
    >
      <ComponentLoader
        v-for="(component, index) in config.dashboard.components"
        :key="index"
        :type="component.type"
        :config="component"
      />
    </div>
  </main>

  <div class="fixed bottom-5 left-5 text-sm">
    <span class="mdi mdi-refresh text-lighter mr-2" />
    <span class="text-dark font-medium">
      {{ format(new Date(), 'dd.MM.yy - HH:mm') }}
    </span>
  </div>
</template>
