<script setup>
import { twMerge } from 'tailwind-merge';

defineProps({
  type: {
    type: String,
    required: true,
  },
  cardStyle: {
    type: String,
    required: false,
    default: '',
  },
});
</script>

<template>
  <section
    :class="[twMerge('card flex flex-col overflow-hidden', cardStyle)]"
    :data-type="type"
  >
    <slot />
  </section>
</template>
