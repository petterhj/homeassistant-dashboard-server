<script setup>
import { useDashboard } from '@/stores/dashboard';
import { useHomeAssistant } from '@/stores/homeassistant';

import ComponentLoader from '../components/ComponentLoader.vue';

const { dashboard } = useDashboard();
const { config, getEntityState } = useHomeAssistant();

// const sun = await getEntityState('sun.sun');
</script>

<template>
  <main v-if="dashboard">
    <ComponentLoader
      v-for="(component, index) in dashboard.components"
      :key="index"
      :type="component.type"
      :config="component"
    />
    <!-- {{ sun }} -->
    <!-- {{ entities }} -->
    <!-- <section class="flex flex-col gap-2">
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
    </section> -->
  </main>

  <div v-if="config" class="fixed bottom-5 left-5 text-gray-400 text-sm">
    <span class="mdi mdi-refresh text-gray-300 mr-2" />
    <span v-if="config.version">{{ config.version }}</span>
    <span v-else>Unknown</span>
  </div>
</template>
