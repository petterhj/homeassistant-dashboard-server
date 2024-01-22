<script setup>
import { computed } from 'vue';
import { format, parseISO } from 'date-fns';
import { useI18n } from 'vue-i18n';
import { getWeatherStateIcon, getWindBearing } from '@/util/ha.weather';
import { useHomeAssistant } from '@/stores/homeassistant';
import { useCard } from '@/composables/card';
import { BASE_CARD_PROPS } from '@/util/card';
import BaseCard from '@/components/generic/BaseCard.vue';

const { t } = useI18n();
const { getEntity, getServiceResponse } = useHomeAssistant();

const props = defineProps({
  ...BASE_CARD_PROPS,
  entity: {
    type: String,
    required: true,
  },
  state: {
    type: Boolean,
    required: false,
    default: true,
  },
  forecast: {
    type: [Boolean, String],
    required: false,
    default: 'hourly',
    validator(value) {
      if (typeof value === 'string') {
        return ['daily', 'hourly'].includes(value);
      }
    },
  },
});

const card = useCard(props, {
  title: t('weather.forecast'),
  icon: 'weather-partly-cloudy',
});
const entity = await getEntity(props.entity);

const forecastData = (
  props.forecast
    ? await getServiceResponse('weather', 'get_forecasts', props.entity, {
        type: typeof props.forecast === 'string' ? props.forecast : 'hourly',
      })
    : {}
)?.forecast;

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
  // if (sun_entity.state) {
  //   if (!datetime && sun_entity.state == 'below_horizon') {
  //     return true;
  //   } else if (datetime) {
  //     const dt = parseISO(datetime);
  //     const currentStateDate = parseISO(sun_entity.last_changed);
  //     const nextRising = parseISO(sun_entity.attributes.next_rising);
  //     const nextSetting = parseISO(sun_entity.attributes.next_setting);

  //     if (
  //       isWithinInterval(dt, {
  //         start: startOfDay(currentStateDate),
  //         end: endOfDay(currentStateDate),
  //       })
  //     ) {
  //       console.log('------------')
  //       console.log(dt);
  //       console.log(currentStateDate);
  //       console.log(nextRising);
  //     }
  //   }
  // }
  return false;
}

function formattedWeatherCondition(state) {
  // if (state === 'partlycloudy') return 'Partly cloudy';
  // state = state.replace('-', ' ');
  // state = state.charAt(0).toUpperCase() + state.slice(1);
  // return state;
  return t('weather.states.' + state, state);
}

function formattedDatetime(datetime) {
  return format(parseISO(datetime), props.forecast === 'daily' ? 'ccc' : 'HH:mm');
}
</script>

<template>
  <BaseCard v-bind="card">
    <!-- State -->
    <div v-if="state" class="flex items-center gap-4">
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
        <div class="flex gap-4 justify-end text-light">
          <span v-if="entity.attributes.wind_speed" class="flex gap-2">
            <span class="mdi mdi-weather-windy text-light"></span>
            <span class="font-medium">
              {{ windSpeedFormattedMs }}
              ({{ getWindBearing(entity.attributes.wind_bearing) }})
            </span>
          </span>
          <span v-if="entity.attributes.precipitation" class="flex gap-2">
            <span class="mdi mdi-weather-rainy text-light"></span>
            <span class="font-medium">
              {{ entity.attributes.precipitation }}
              {{ entity.attributes.precipitation_unit }}
            </span>
          </span>
        </div>
      </div>
    </div>

    <!-- Forecast -->
    <div v-if="forecastData" class="mt-4 flex flex-row justify-between">
      <div
        v-for="measurement in forecastData.slice(0, 5)"
        :key="measurement.datetime"
        class="flex flex-col gap-1 items-center"
      >
        <span class="text-sm capitalize font-medium">
          {{ formattedDatetime(measurement.datetime) }}
        </span>
        <div
          class="h-8 w-8"
          v-html="
            getWeatherStateIcon(measurement.condition, isNightTime(measurement.datetime))
          "
        />
        <span class="text-sm font-semibold">
          {{ measurement.temperature }} {{ entity.attributes.temperature_unit }}
        </span>
      </div>
    </div>
  </BaseCard>
</template>
