<script setup>
import { computed } from 'vue';
import { format, parseISO, isWithinInterval, startOfDay, endOfDay } from 'date-fns';
import { useI18n } from 'vue-i18n';
import { getWeatherStateIcon, getWindBearing } from '@/util/ha.weather';
import { useEntity } from '@/composables/entity.js';

import BaseCard from './BaseCard.vue';

const props = defineProps({
  entityId: {
    type: String,
    required: true,
  },
  hideState: {
    type: Boolean,
    required: false,
    default: false,
  },
  hideForecast: {
    type: Boolean,
    required: false,
    default: false,
  },
  dateFormat: {
    type: String,
    required: false,
    default: 'ccc',
  },
});

const { t } = useI18n();
const entity = useEntity(props.entityId);
const sun_entity = useEntity('sun.sun');

const windSpeedFormattedMs = computed(() => {
  const windSpeed = entity.attributes?.wind_speed;
  if (windSpeed) {
    if (windSpeed) {
      return (windSpeed * 0.27777777777778).toFixed(1) + ' m/s';
    }
    return windSpeed + ' m/s';
  }
  return null;
});

// const isNightTime = computed(() => {
//   if (sun_entity.state) {
//     return true;
//   }
//   return false;
// });

function isNightTime(datetime) {
  if (sun_entity.state) {
    if (!datetime && sun_entity.state == 'below_horizon') {
      return true;
    } else if (datetime) {
      const dt = parseISO(datetime);
      const currentStateDate = parseISO(sun_entity.last_changed);
      const nextRising = parseISO(sun_entity.attributes.next_rising);
      const nextSetting = parseISO(sun_entity.attributes.next_setting);

      if (
        isWithinInterval(dt, {
          start: startOfDay(currentStateDate),
          end: endOfDay(currentStateDate),
        })
      ) {
        console.log('------------')
        console.log(dt);
        console.log(currentStateDate);
        console.log(nextRising);
      }
    }
  }
  return false;
}

function formattedWeatherCondition(state) {
  // if (state === 'partlycloudy') return 'Partly cloudy';
  // state = state.replace('-', ' ');
  // state = state.charAt(0).toUpperCase() + state.slice(1);
  // return state;
  return t('weather.states.' + state, state);
}
</script>

<template>
  <BaseCard :entity="entity">
    <!-- State -->
    <div v-if="entity.state && !hideState" class="flex items-center gap-4">
      <div
        class="h-12 w-12 mt-2"
        v-html="getWeatherStateIcon(entity.state, isNightTime())"
      />

      <span class="text-2xl font-semibold flex-1">
        {{ formattedWeatherCondition(entity.state) }}
      </span>

      <div class="flex flex-col">
        <span class="text-2xl font-bold text-right">
          {{ entity.attributes.temperature }} {{ entity.attributes.temperature_unit }}
        </span>
        <div class="flex gap-4 justify-end text-gray-600">
          <span v-if="entity.attributes.wind_speed" class="flex gap-2">
            <span class="mdi mdi-weather-windy text-gray-400"></span>
            <span class="font-medium">
              {{ windSpeedFormattedMs }}
              ({{ getWindBearing(entity.attributes.wind_bearing) }})
            </span>
          </span>
          <span v-if="entity.attributes.precipitation" class="flex gap-2">
            <span class="mdi mdi-weather-rainy text-gray-400"></span>
            <span class="font-medium">
              {{ entity.attributes.precipitation }}
              {{ entity.attributes.precipitation_unit }}
            </span>
          </span>
        </div>
      </div>
    </div>

    <!-- Forecast -->
    <div
      v-if="entity.attributes && !hideForecast"
      class="mt-4 flex flex-row justify-between"
    >
      <div
        v-for="measurement in entity.attributes.forecast.slice(0, 5)"
        :key="measurement.datetime"
        class="flex flex-col gap-1 items-center"
      >
        <span class="text-sm capitalize">
          {{ format(parseISO(measurement.datetime), dateFormat) }}
        </span>
        <div
          class="h-8 w-8"
          v-html="
            getWeatherStateIcon(measurement.condition, isNightTime(measurement.datetime))
          "
        />
        <span class="text-sm font-medium">
          {{ measurement.temperature }} {{ entity.attributes.temperature_unit }}
        </span>
        <!-- <span>{{ measurement.precipitation_probability }}</span> -->
      </div>
    </div>
  </BaseCard>
</template>
