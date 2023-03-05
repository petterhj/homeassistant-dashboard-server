<script setup>
import { format } from 'date-fns';
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

  <div v-if="config" class="fixed bottom-5 left-5 text-sm">
    <span class="mdi mdi-refresh text-gray-300 mr-2" />
    <span class="text-gray-400 font-medium">
      {{ format(new Date(), 'dd.MM.yy - HH:mm') }}
    </span>
    <span class="text-gray-300" v-if="config.version"> ({{ config.version }})</span>
  </div>
</template>
