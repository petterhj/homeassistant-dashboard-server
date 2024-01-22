<script setup>
import { format } from 'date-fns';
import { useServer } from '@/stores/server';

import ComponentLoader from '../components/ComponentLoader.vue';

const { config } = useServer();
</script>

<template>
  <main class="h-[calc(100%-2rem)]">
    <div
      class="h-full flex flex-col gap-4 p-4 pb-0"
      v-if="config?.dashboard?.components?.length"
    >
      <ComponentLoader
        v-for="(component, index) in config.dashboard.components"
        :key="index"
        :type="component.type"
        :config="component"
      />
    </div>
  </main>
  <footer class="h-8 px-4 leading-8 text-sm">
    <span class="mdi mdi-refresh text-lighter mr-2" />
    <span class="text-dark font-medium">
      {{ format(new Date(), 'dd.MM.yy - HH:mm') }}
    </span>
  </footer>
</template>

<style>
.card {
  border: 4px solid blue;
  flex: 1 0 auto;
  height: 0px;
  overflow: hidden;
}
</style>
