<script setup>
import { useRoute } from 'vue-router';
import { BASE_CARD_PROPS } from '@/util/card';
import CardTitle from './CardTitle.vue';

defineProps(BASE_CARD_PROPS);

const { query } = useRoute();
</script>

<template>
  <section
    :class="cardStyle"
    :data-type="type"
    :style="[query?.debug === 'true' ? { background: '#EFEFEF' } : null]"
  >
    <CardTitle v-if="title" :title="title" :icon="icon" />
    <slot />
  </section>
</template>
