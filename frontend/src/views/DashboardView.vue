<script setup>
import { useEntity } from '@/composables/entity.js';

import WeatherForecastCard from '../components/cards/WeatherForecastCard.vue';
import WeatherGraphCard from '../components/cards/WeatherGraphCard.vue';
import CalendarCard from '../components/cards/CalendarCard.vue';
import ListCard from '../components/cards/ListCard.vue';
import SunCard from '../components/cards/SunCard.vue';

const currentTime = useEntity('sensor.date_time');
</script>

<template>
  <main>
    <section class="flex flex-col gap-2">
      <WeatherForecastCard entity-id="weather.oslo" :hide-forecast="true" />
      <WeatherForecastCard
        entity-id="weather.oslo_hourly"
        :hide-state="true"
        date-format="HH:mm"
      />
      <WeatherGraphCard
        entity-id="weather.oslo_hourly"
        attribute="temperature"
        date-format="HH"
        class="h-48"
      />
      <SunCard entity-id="sun.sun" class="h-16" />
      <WeatherForecastCard entity-id="weather.oslo" :hide-state="true" />
      <hr />
    </section>

    <section class="flex flex-col gap-2">
      <div class="h-64 bg-gray-100"></div>
      <hr />
      <ListCard
        entity-id="sensor.handleliste"
        title-attribute="friendly_name"
        items-attribute="items"
        title-prop="content"
        icon="cart-outline"
        icon-item="leek"
      />
    </section>

    <section>
      <CalendarCard
        title="Kalender"
        icon="calendar-blank"
        class="h-full"
        :icon-items="{
          'calendar.loppemarkeder': 'package-variant',
        }"
      />
    </section>
  </main>

  <div v-if="currentTime" class="fixed bottom-5 left-5 text-gray-400 text-sm">
    <span class="mdi mdi-refresh text-gray-300 mr-2" />
    <span v-if="currentTime.state">{{ currentTime.state }}</span>
    <span v-else>Unknown</span>
  </div>
</template>
