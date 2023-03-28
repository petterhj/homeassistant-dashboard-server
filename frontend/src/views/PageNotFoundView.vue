<script setup>
import { useI18n } from 'vue-i18n';
import EmptyState from '../components/ErrorState.vue';

const { t } = useI18n();
</script>

<template>
  <EmptyState :title="t('general.pageNotFound')" message="404" />
</template>
