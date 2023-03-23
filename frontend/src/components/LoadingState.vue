<script setup>
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

defineProps({
  message: {
    type: String,
    required: false,
    default: null,
  },
});
</script>

<template>
  <div class="h-full p-4 flex flex-col gap-2 items-center justify-center bg-lightest">
    <span class="mdi mdi-refresh text-4xl text-light" />
    <span class="font-semibold">
      {{ t('general.loading') }}
    </span>
    <span v-if="message" class="text-sm text-light">
      {{ message }}
    </span>
  </div>
</template>
