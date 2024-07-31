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
  componentType: {
    type: String,
    required: false,
    default: null,
  },
});
</script>

<template>
  <div
    class="
      error-card
      relative
      p-4 min-h-24
      flex flex-col gap-2 items-center justify-center
      bg-lightest
    "
  >
    <span class="absolute bottom-1 left-1 flex items-center text-lighter text-xs">
      {{ componentType }}
    </span>

    <span
      class="mdi text-lighter"
      :class="[`mdi-${icon}`, size === 'large' ? 'text-8xl' : 'text-4xl']"
    />
    <span class="font-semibold">
      {{ title }}
    </span>
    <span v-if="error" class="text-sm text-light text-center">
      {{ error.message }}
    </span>
    <span v-if="error?.errors" class="text-sm font-mono text-lighter">
      <span v-for="e in error.errors" :key="e.location">
        {{ e.location }}: {{ e.message }}
      </span>
    </span>
  </div>
</template>

<style scoped>
.error-card {
  flex: 1 0 auto;
  height: 0px;
  overflow: hidden;
}
</style>
