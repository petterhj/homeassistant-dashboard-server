<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useIntersectionObserver } from '@vueuse/core';
import { BASE_CARD_PROPS } from '@/util/card';
import CardTitle from './CardTitle.vue';

defineProps(BASE_CARD_PROPS);

const { query } = useRoute();

const card = ref(null);
const cardContent = ref(null);
const isOverflowing = ref(false);

useIntersectionObserver(
  cardContent,
  ([{ isIntersecting }]) => {
    isOverflowing.value = !isIntersecting;
  },
  {
    root: card,
    rootMargin: '5px 2500px', // Trigger for height only
    threshold: 1.0,
  }
);
</script>

<template>
  <section
    ref="card"
    :class="[
      'card',
      cardStyle,
      { 'card--overflow': isOverflowing },
      { 'card--debug': query?.debug },
    ]"
    :data-type="type"
  >
    <CardTitle v-if="title" :title="title" :icon="icon" />
    <div ref="cardContent" class="card-content">
      <slot />
    </div>
  </section>
</template>

<style scoped>
.card--overflow {
  position: relative;
}
.card--overflow::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    180deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0) 89%,
    rgba(255, 255, 255, 1) 98%,
    rgba(255, 255, 255, 1) 100%
  );
}
.card--debug {
  background: #efefef;
}
.card--overflow.card--debug {
  background: rgb(249, 234, 236);
}
</style>
