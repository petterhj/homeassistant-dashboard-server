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
  <h1 v-if="title" class="text-md text-light font-bold uppercase">
    <span v-if="icon" class="mdi text-light mr-1" :class="['mdi-' + icon]" />
    {{ title }}
  </h1>
  <hr />
</template>
