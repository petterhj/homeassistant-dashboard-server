<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  icon: {
    type: String,
    required: false,
    default: null,
  },
});
</script>

<template>
  <h1 v-if="title" class="mb-3 text-md text-gray-400 font-semibold uppercase">
    <span v-if="icon" class="mdi text-gray-400 mr-1" :class="['mdi-' + icon]" />
    {{ title }}
  </h1>
</template>
