<script setup>
import { useDashboard } from '@/stores/dashboard';
import { useHomeAssistant } from '@/stores/homeassistant';

import ComponentLoader from '../components/ComponentLoader.vue';

const { dashboard } = useDashboard();
const { config } = useHomeAssistant();
</script>

<template>
  <main v-if="dashboard">
    <ComponentLoader
      v-for="(component, index) in dashboard.components"
      :key="index"
      :type="component.type"
      :config="component"
    />
  </main>

  <div v-if="config" class="fixed bottom-5 left-5 text-gray-400 text-sm">
    <span class="mdi mdi-refresh text-gray-300 mr-2" />
    <span v-if="config.version">{{ config.version }}</span>
    <span v-else>Unknown</span>
  </div>
</template>
