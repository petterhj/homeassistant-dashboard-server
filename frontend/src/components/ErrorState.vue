<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  message: {
    type: String,
    required: false,
    default: null,
  },
  icon: {
    type: String,
    required: false,
    default: 'alert-octagram',
  },
});
</script>

<template>
  <div class="h-full p-4 flex flex-col gap-2 items-center justify-center bg-gray-200">
    <span class="mdi text-4xl text-gray-300" :class="`mdi-${icon}`" />
    <span class="font-semibold">
      {{ title }}
    </span>
    <span v-if="message" class="text-sm text-gray-400">
      {{ message }}
    </span>
  </div>
</template>
