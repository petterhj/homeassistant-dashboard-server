<script setup>
defineProps({
  entity: {
    type: Object,
    required: true,
  },
  height: {
    type: Number,
    required: false,
    default: 64,
  },
});
</script>

<template>
  <section
    class="flex flex-col"
    :class="[{ 'bg-gray-200': !entity.state }]"
  >
    <slot v-if="entity.state" />

    <div v-else class="h-full flex flex-col gap-1 justify-center text-center">
      <span class="mdi mdi-alert-decagram text-gray-400 text-4xl"></span>
      <span class="text-lg font-semibold">{{ entity.id }}</span>
      <span class="font-medium text-gray-500"> Could not load entity state</span>
      <span class="text-xs text-gray-400 italic mx-6">{{ entity.error }}</span>
    </div>
  </section>
</template>
