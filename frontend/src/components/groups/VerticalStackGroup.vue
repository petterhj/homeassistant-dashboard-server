<script setup>
import { twMerge } from 'tailwind-merge';

defineProps({
  cardStyle: {
    type: String,
    required: false,
    default: '',
  },
});
</script>

<template>
  <section
    data-type="vertical-stack-group"
    :class="twMerge('flex flex-col gap-4 overflow-hidden', cardStyle)"
  >
    <slot />
  </section>
</template>
