<script setup>
import { useI18n } from 'vue-i18n';
import { useServer } from '@/stores/server';
import EmptyState from '../components/ErrorState.vue';
import ComponentLoader from '../components/ComponentLoader.vue';

const { t } = useI18n();
const { currentView } = useServer();
</script>

<template>
  <template v-if="currentView && currentView.components?.length">
    <ComponentLoader
      v-for="(component, index) in currentView.components"
      :key="index"
      :type="component.type"
      :config="component"
    />
  </template>
  <EmptyState v-else-if="currentView" :title="t('errors.viewNotConfigured')" />
  <EmptyState v-else :title="t('errors.viewNotFound')" />
</template>
