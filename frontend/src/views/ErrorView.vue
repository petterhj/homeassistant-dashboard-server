<script setup>
import { useI18n } from 'vue-i18n';
import EmptyState from '../components/ErrorState.vue';

const { t } = useI18n();

const icon = history.state?.icon;
const messageKey = history.state?.messageKey || 'errors.pageNotFound';
</script>

<template>
  <EmptyState :title="t(messageKey)" :icon="icon" />
</template>

