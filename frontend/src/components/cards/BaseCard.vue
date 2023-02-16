<script setup>
defineProps({
  error: {
    type: String,
    required: false,
  },
  title: {
    type: String,
    required: false,
    default: null,
  },
  icon: {
    type: String,
    required: false,
    default: null,
  },
});
</script>

<template>
  <section class="card flex flex-col overflow-hidden" :class="[{ 'bg-gray-200': error }]">
    <template v-if="!error">
      <h1 v-if="title" class="mb-4 text-1xl text-gray-400 font-semibold mb-2 uppercase">
        <span v-if="icon" class="mdi text-gray-400 mr-1" :class="['mdi-' + icon]" />
        {{ title }}
      </h1>
      <slot />
    </template>

    <div v-else class="h-full flex flex-col gap-1 justify-center text-center">
      <span class="mdi mdi-alert-decagram text-gray-400 text-4xl" />
      <!-- <span class="text-lg font-semibold">{{ entity.id }}</span> -->
      <span class="font-medium text-gray-500"> Could not load data</span>
      <span class="text-xs text-gray-400 italic mx-6">{{ error }}</span>
    </div>
  </section>
</template>
