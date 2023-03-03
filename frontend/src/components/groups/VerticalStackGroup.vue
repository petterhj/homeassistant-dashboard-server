<script setup>
defineProps({
  cardStyle: {
    type: String,
    required: false,
    default: '',
  },
});
</script>

<template>
  <section :class="['flex', 'flex-col', cardStyle]">
    <slot />
  </section>
</template>
