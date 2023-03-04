<script setup>
import { formatDistance, parseISO } from 'date-fns';
import { useHomeAssistant } from '@/stores/homeassistant';
import CardTitle from './partials/CardTitle.vue';

const { getEntities } = useHomeAssistant();

const props = defineProps({
  entities: {
    type: Array,
    required: true,
  },
  display: {
    type: String,
    required: false,
    default: 'list',
    validator: (val) => ['list', 'grid'].includes(val),
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

const states = await getEntities(
  props.entities.map((entityConfig) => entityConfig.entity)
);

const getIcon = (entityConfig) => {
  if (entityConfig.icon) {
    return 'mdi-' + entityConfig.icon;
  }
  const stateData = states[entityConfig.entity];
  const icon = stateData?.attributes?.icon;
  if (icon) {
    return icon.replace(':', '-');
  }
  return 'mdi-lightning-bolt';
};
const getName = (entityConfig) => {
  if (entityConfig.name) {
    return entityConfig.name;
  }
  const stateData = states[entityConfig.entity];
  const friendlyName = stateData?.attributes?.friendly_name;
  return friendlyName;
};
const getSecondaryInfo = (entityConfig) => {
  // https://www.home-assistant.io/dashboards/entities/#secondary_info
  const stateData = states[entityConfig.entity];

  if (entityConfig.secondaryInfo && entityConfig.secondaryInfo.startsWith('attribute.')) {
    const attribute = entityConfig.secondaryInfo.replace('attribute.', '');
    if (stateData?.attributes[attribute]) {
      return stateData.attributes[attribute];
    } else {
      return '?';
    }
  }

  switch (entityConfig.secondaryInfo) {
    case 'last-changed':
      return `${formatDistance(new Date(), parseISO(stateData.lastChanged))} ago`;
    case 'last-updated':
      return `${formatDistance(new Date(), parseISO(stateData.lastUpdated))} ago`;
    default:
      return '';
  }
};
const getValue = (entityConfig) => {
  const stateData = states[entityConfig.entity];

  if (entityConfig.attribute && stateData?.attributes) {
    const attrValue = stateData?.attributes[entityConfig.attribute];
    if (attrValue) {
      return entityConfig.unit ? `${attrValue} ${entityConfig.unit}` : attrValue;
    }
    return '?';
  }

  const stateClass = states[entityConfig.entity]?.attributes?.state_class;
  let state = stateData.state;
  if (stateClass && !isNaN(parseFloat(state))) {
    // `state_class`: Type of state. If not None, the sensor is assumed to be numerical.
    // https://developers.home-assistant.io/docs/core/entity/sensor/#properties
    const precision = entityConfig.precision || 0;
    state = parseFloat(state).toFixed(precision);
  }
  const unitOfMeasurement = entityConfig.unit
    ? entityConfig.unit
    : stateData?.attributes?.unit_of_measurement;
  return unitOfMeasurement ? `${state} ${unitOfMeasurement}` : state;
};
</script>

<template>
  <CardTitle v-if="title" :title="title" :icon="icon" />

  <template v-if="display === 'list'">
    <div class="flex flex-col gap-2">
      <template
        v-for="(entityConfig, index) in entities"
        :key="`${entityConfig.entity}_${index}`"
      >
        <div v-if="entityConfig.entity in states" class="flex gap-3 items-center text-sm">
          <span>
            <span class="mdi text-gray-400 text-lg" :class="getIcon(entityConfig)"></span>
          </span>
          <span class="flex flex-col">
            <span class="font-medium">
              {{ getName(entityConfig) }}
            </span>
            <span class="text-xs text-gray-400">
              {{ getSecondaryInfo(entityConfig) }}
            </span>
          </span>
          <span class="flex-grow text-right">
            {{ getValue(entityConfig) }}
          </span>
        </div>
      </template>
    </div>
  </template>

  <template v-if="display === 'grid'">
    <div class="grid grid-cols-2 gap-4">
      <template
        v-for="(entityConfig, index) in entities"
        :key="`${entityConfig.entity}_${index}`"
      >
        <div v-if="entityConfig.entity in states" class="d-stat inline p-0">
          <div class="d-stat-title text-xs">
            <span class="mdi text-gray-400" :class="getIcon(entityConfig)"></span>
            {{ getName(entityConfig) }}
          </div>
          <div class="d-stat-value px-1 text-lg font-semibold">
            {{ getValue(entityConfig) }}
          </div>
          <div class="d-stat-desc px-1 text-xs">
            {{ getSecondaryInfo(entityConfig) }}
          </div>
        </div>
      </template>
    </div>
  </template>
</template>
