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
  <div class="h-full p-4 flex flex-col gap-2 items-center justify-center bg-gray-200">
    <span class="mdi mdi-refresh text-4xl text-gray-300" />
    <span class="font-semibold">
      {{ t('general.loading') }}
    </span>
    <span v-if="message" class="text-sm text-gray-500">
      {{ message }}
    </span>
  </div>
</template>
