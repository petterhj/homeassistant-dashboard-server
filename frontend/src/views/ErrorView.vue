<script setup>
// import { useEntity } from '@/composables/entity.js';

// import WeatherForecastCard from '../components/cards/WeatherForecastCard.vue';
// import WeatherGraphCard from '../components/cards/WeatherGraphCard.vue';
// import ListCard from '../components/cards/ListCard.vue';

// const currentTime = useEntity('sensor.date_time');
</script>

<template>
  <main class="flex flex-col justify-center items-center gap-6">
    <RouterLink :to="{ name: 'dashboard' }">
      <span class="mdi mdi-cat text-gray-400 text-9xl"></span>
    </RouterLink>
    <span class="text-xl font-medium">Could not connect to Home Assistant</span>
  </main>
</template>
