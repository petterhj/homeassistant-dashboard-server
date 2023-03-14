<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  error: {
    type: Error,
    required: false,
    default: null,
  },
  icon: {
    type: String,
    required: false,
    default: 'alert-octagram',
  },
  size: {
    type: String,
    required: false,
    default: 'small',
  },
});
</script>

<template>
  <div class="h-full p-4 flex flex-col gap-2 items-center justify-center bg-gray-200">
    <span
      class="mdi text-gray-300"
      :class="[`mdi-${icon}`, size === 'large' ? 'text-8xl' : 'text-4xl']"
    />
    <span class="font-semibold">
      {{ title }}
    </span>
    <span v-if="error" class="text-sm text-gray-500">
      {{ error.message }}
    </span>
    <span v-if="error?.errors" class="text-sm font-mono text-gray-400">
      <span v-for="error in error.errors" :key="error.location">
        {{ error.location }}: {{ error.message }}
      </span>
    </span>
  </div>
</template>
