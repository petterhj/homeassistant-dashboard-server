<script setup>
// (Un)shamefully lifted from Home assistant Sun card:
//  https://github.com/AitorDB/home-assistant-sun-card/
import { computed, ref } from 'vue';
import { format, parseISO } from 'date-fns';
import { useI18n } from 'vue-i18n';
import { useHomeAssistant } from '@/stores/homeassistant';
import { useCard } from '@/composables/card';
import { BASE_CARD_PROPS } from '@/util/card';
import BaseCard from '@/components/generic/BaseCard.vue';

const { t } = useI18n();
const { getEntity } = useHomeAssistant();

const props = defineProps({
  ...BASE_CARD_PROPS,
  entity: {
    type: String,
    required: false,
    default: 'sun.sun',
  },
});

const entity = await getEntity(props.entity);
const card = useCard(props, {
  title: t('sun.sun'),
  icon: entity?.state === 'below_horizon' ? 'weather-night' : 'white-balance-sunny',
});
const sunLine = ref(null);

const EVENT_X_POSITIONS = {
  dayStart: 5,
  sunrise: 101,
  sunset: 449,
  dayEnd: 545,
};
const HORIZON_Y = 108;
const SUN_RADIUS = 17;

const generateId = () => {
  return Math.random().toString(36).replace('0.', '');
};

const convertDateToMinutesSinceDayStarted = (date) => {
  return date.getHours() * 60 + date.getMinutes();
};

const ids = {
  sun: generateId(),
  dawn: generateId(),
  day: generateId(),
  dusk: generateId(),
};

const sunData = computed(() => {
  if (!entity || !sunLine.value) {
    return null;
  }
  const sunrise = new Date(entity.attributes.next_rising);
  const sunset = new Date(entity.attributes.next_setting);
  const eventsAt = {
    dayStart: 0,
    sunrise: convertDateToMinutesSinceDayStarted(sunrise),
    sunset: convertDateToMinutesSinceDayStarted(sunset),
    dayEnd: 23 * 60 + 59,
  };
  const now = new Date();
  const minutesSinceTodayStarted = convertDateToMinutesSinceDayStarted(now);

  // Dawn section position [0 - 105]
  const dawnSectionPosition =
    (Math.min(minutesSinceTodayStarted, eventsAt.sunrise) * 105) / eventsAt.sunrise;

  // Day section position [106 - 499]
  const minutesSinceDayStarted = Math.max(minutesSinceTodayStarted - eventsAt.sunrise, 0);
  const daySectionPosition =
    (Math.min(minutesSinceDayStarted, eventsAt.sunset - eventsAt.sunrise) * (499 - 106)) /
    (eventsAt.sunset - eventsAt.sunrise);

  // Dusk section position [500 - 605]
  const minutesSinceDuskStarted = Math.max(minutesSinceTodayStarted - eventsAt.sunset, 0);
  const duskSectionPosition =
    (minutesSinceDuskStarted * (605 - 500)) / (eventsAt.dayEnd - eventsAt.sunset);

  const position = dawnSectionPosition + daySectionPosition + duskSectionPosition;
  const sunPosition = sunLine.value.getPointAtLength(position);

  const dawnProgressPercent =
    (100 * (sunPosition.x - EVENT_X_POSITIONS.dayStart)) /
    (EVENT_X_POSITIONS.sunrise - EVENT_X_POSITIONS.dayStart);
  const dayProgressPercent =
    (100 * (sunPosition.x - EVENT_X_POSITIONS.sunrise)) /
    (EVENT_X_POSITIONS.sunset - EVENT_X_POSITIONS.sunrise);
  const duskProgressPercent =
    (100 * (sunPosition.x - EVENT_X_POSITIONS.sunset)) /
    (EVENT_X_POSITIONS.dayEnd - EVENT_X_POSITIONS.sunset);

  const sunYTop = sunPosition.y - SUN_RADIUS;
  const yOver = HORIZON_Y - sunYTop;
  let sunPercentOverHorizon = 0;
  if (yOver > 0) {
    sunPercentOverHorizon = Math.min((100 * yOver) / (2 * SUN_RADIUS), 100);
  }

  return {
    dawnProgressPercent,
    dayProgressPercent,
    duskProgressPercent,
    sunPercentOverHorizon,
    sunPosition: { x: sunPosition.x, y: sunPosition.y },
    times: {
      dawn: parseISO(entity.attributes.next_dawn),
      dusk: parseISO(entity.attributes.next_dusk),
      noon: parseISO(entity.attributes.next_noon),
      sunrise: parseISO(entity.attributes.next_rising),
      sunset: parseISO(entity.attributes.next_setting),
    },
  };
});
</script>

<template>
  <BaseCard v-bind="card">
    <div class="flex flex-col gap-2 text-sm">
      <div v-if="sunData" class="flex justify-between px-6">
        <div class="text-center">
          <span class="block font-medium">{{ t('sun.sunrise') }}</span>
          {{ format(sunData.times.sunrise, 'HH:mm') }}
        </div>
        <div class="text-center">
          <span class="block font-medium">{{ t('sun.sunset') }}</span>
          {{ format(sunData.times.sunset, 'HH:mm') }}
        </div>
      </div>
      <div class="-mt-12">
        <svg viewBox="0 0 550 150" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient :id="ids.sun" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" style="stop-color: #333333; stop-opacity: 1" />
              <stop
                :offset="`${sunData?.sunPercentOverHorizon ?? 0}%`"
                style="stop-color: #333333; stop-opacity: 1"
              />
              <stop
                :offset="`${sunData?.sunPercentOverHorizon ?? 0}%`"
                style="stop-color: rgb(0, 0, 0, 0); stop-opacity: 1"
              />
            </linearGradient>

            <linearGradient :id="ids.dawn" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop
                offset="0%"
                style="stop-color: rgb(var(--color-lighter)); stop-opacity: 1"
              />
              <stop
                :offset="`${sunData?.dawnProgressPercent ?? 0}%`"
                style="stop-color: rgb(var(--color-lighter)); stop-opacity: 1"
              />
              <stop
                :offset="`${sunData?.dawnProgressPercent ?? 0}%`"
                style="stop-color: rgb(0, 0, 0, 0); stop-opacity: 1"
              />
            </linearGradient>

            <linearGradient :id="ids.day" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop
                offset="0%"
                style="stop-color: rgb(var(--color-lightest)); stop-opacity: 1"
              />
              <stop
                :offset="`${sunData?.dayProgressPercent ?? 0}%`"
                style="stop-color: rgb(var(--color-lightest)); stop-opacity: 1"
              />
              <stop
                :offset="`${sunData?.dayProgressPercent ?? 0}%`"
                style="stop-color: rgb(0, 0, 0, 0); stop-opacity: 1"
              />
            </linearGradient>

            <linearGradient :id="ids.dusk" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop
                offset="0%"
                style="stop-color: rgb(var(--color-lighter)); stop-opacity: 1"
              />
              <stop
                :offset="`${sunData?.duskProgressPercent ?? 0}%`"
                style="stop-color: rgb(var(--color-lighter)); stop-opacity: 1"
              />
              <stop
                :offset="`${sunData?.duskProgressPercent ?? 0}%`"
                style="stop-color: rgb(0, 0, 0, 0); stop-opacity: 1"
              />
            </linearGradient>
          </defs>
          <path
            ref="sunLine"
            class="sun-card-sun-line"
            d="M5,146 C29,153 73,128 101,108 C276,-29 342,23 449,108 C473,123 509,150 545,146"
            fill="none"
            stroke="#DFDFDF"
            shape-rendering="geometricPrecision"
          />
          <path
            d="M5,146 C29,153 73,128 101,108 L 5 108"
            :fill="`url(#${ids.dawn})`"
            :opacity="sunData?.dawnProgressPercent ? 1 : 0"
            :stroke="`url(#${ids.dawn})`"
            shape-rendering="geometricPrecision"
          />
          <path
            d="M101,108 C276,-29 342,23 449,108 L 104,108"
            :fill="`url(#${ids.day})`"
            :opacity="sunData?.dayProgressPercent ? 1 : 0"
            :stroke="`url(#${ids.day})`"
            shape-rendering="geometricPrecision"
          />
          <path
            d="M449,108 C473,123 509,150 545,146 L 545 108"
            :fill="`url(#${ids.dusk})`"
            :opacity="sunData?.duskProgressPercent ? 1 : 0"
            :stroke="`url(#${ids.dusk})`"
            shape-rendering="geometricPrecision"
          />
          <line x1="5" y1="108" x2="545" y2="108" stroke="#333333" />
          <!-- <line x1="101" y1="25" x2="101" y2="100" stroke="#333333" /> -->
          <!-- <line x1="449" y1="25" x2="449" y2="100" stroke="#333333" /> -->
          <circle
            :cx="`${sunData?.sunPosition.x ?? 0}`"
            :cy="`${sunData?.sunPosition.y ?? 0}`"
            r="17"
            :opacity="sunData?.sunPercentOverHorizon ? 1 : 0"
            stroke="none"
            :fill="`url(#${ids.sun})`"
            shape-rendering="geometricPrecision"
          />
        </svg>
      </div>
      <div v-if="sunData" class="flex justify-between px-4">
        <div class="text-center">
          <span class="block font-medium">{{ t('sun.dawn') }}</span>
          {{ format(sunData.times.dawn, 'HH:mm') }}
        </div>
        <div class="text-center">
          <span class="block font-medium">{{ t('sun.solarNoon') }}</span>
          {{ format(sunData.times.noon, 'HH:mm') }}
        </div>
        <div class="text-center">
          <span class="block font-medium">{{ t('sun.dusk') }}</span>
          {{ format(sunData.times.dusk, 'HH:mm') }}
        </div>
      </div>
    </div>
  </BaseCard>
</template>
