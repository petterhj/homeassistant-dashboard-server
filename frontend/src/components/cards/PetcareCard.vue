<script setup>
import { computed } from 'vue';
import { formatDistance, parseISO } from 'date-fns';
import { useI18n } from 'vue-i18n';
import { useHomeAssistant } from '@/stores/homeassistant';
import CardTitle from './partials/CardTitle.vue';

const { t } = useI18n();
const { getEntities } = useHomeAssistant();

const props = defineProps({
  petEntity: {
    type: String,
    required: true,
  },
  hubEntity: {
    type: String,
    required: true,
  },
  flapBatteryEntity: {
    type: String,
    required: true,
  },
  flapConnectivityEntity: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: false,
    default: null,
  },
  icon: {
    type: String,
    required: false,
    default: null,
  },
});

const states = await getEntities([
  props.petEntity,
  props.hubEntity,
  props.flapBatteryEntity,
  props.flapConnectivityEntity,
]);

const flapBatteryIcon = computed(() => {
  const batteryLevel = parseInt(states[props.flapBatteryEntity].state);

  if (batteryLevel > 0 && batteryLevel <= 10) {
    return 'battery-alert-variant-outline';
  } else if (batteryLevel > 10 && batteryLevel <= 20) {
    return 'battery-10';
  } else if (batteryLevel > 20 && batteryLevel <= 30) {
    return 'battery-20';
  } else if (batteryLevel > 30 && batteryLevel <= 40) {
    return 'battery-30';
  } else if (batteryLevel > 40 && batteryLevel <= 50) {
    return 'battery-40';
  } else if (batteryLevel > 50 && batteryLevel <= 60) {
    return 'battery-50';
  } else if (batteryLevel > 60 && batteryLevel <= 70) {
    return 'battery-60';
  } else if (batteryLevel > 70 && batteryLevel <= 80) {
    return 'battery-70';
  } else if (batteryLevel > 80 && batteryLevel <= 90) {
    return 'battery-80';
  } else if (batteryLevel > 90 && batteryLevel <= 95) {
    return 'battery-90';
  } else if (batteryLevel > 95 && batteryLevel <= 100) {
    return 'battery';
  } else {
    return 'battery-unknown';
  }
});
</script>

<template>
  <CardTitle v-if="title" :title="title" :icon="icon" />

  <div class="flex items-center gap-4">
    <div class="d-avatar d-placeholder">
      <div class="bg-lightest rounded-full w-10 h-10">
        <span
          class="mdi text-dark text-2xl"
          :class="`mdi-${states[petEntity].state === 'on' ? 'home' : 'pine-tree'}`"
        />
      </div>
    </div>
    <div class="flex flex-col flex-1">
      <div class="text-lg leading-5 font-semibold">
        {{ t(`petcare.${states[petEntity].state === 'on' ? 'inside' : 'outside'}`) }}
      </div>
      <div class="flex justify-between text-sm font-medium">
        <span class="text-light">
          {{ formatDistance(new Date(), parseISO(states[petEntity].attributes.since)) }}
          {{ t('datetime.ago') }}
        </span>
        <div class="text-light">
          <span
            class="mdi"
            :class="`mdi-${
              states[hubEntity].state === 'on'
                ? 'check-circle-outline'
                : 'alert-circle-outline'
            }`"
          />
          <span
            class="mdi"
            :class="`mdi-${
              states[hubEntity].state === 'on'
                ? 'check-circle-outline'
                : 'alert-circle-outline'
            }`"
          />
          <span class="mdi" :class="`mdi-${flapBatteryIcon}`" />
          <span>{{ states[props.flapBatteryEntity].state }} %</span>
        </div>
      </div>
    </div>
  </div>
</template>
