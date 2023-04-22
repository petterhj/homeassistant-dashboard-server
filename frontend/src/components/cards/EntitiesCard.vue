<script setup>
import { formatDistance, parseISO } from 'date-fns';
import { useI18n } from 'vue-i18n';
import { useHomeAssistant } from '@/stores/homeassistant';
import CardTitle from './partials/CardTitle.vue';

const { t } = useI18n();
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
    validator: (val) => ['list', 'grid', 'grouped'].includes(val),
  },
  columns: {
    type: Number,
    required: false,
    default: 2,
  },
  groups: {
    type: Array,
    required: false,
    default: null,
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
  props.entities
    .map((entityConfig) => entityConfig.entity)
    .concat(
      // Include any entities when used as source for `secondaryInfo`
      props.entities
        .map((entityConfig) => entityConfig.secondaryInfo)
        .filter((source) => source && source.startsWith('sensor.'))
    )
    .filter((value, index, array) => array.indexOf(value) === index)
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
  if (Object.prototype.hasOwnProperty.call(entityConfig, 'name')) {
    return entityConfig.name;
  }
  const stateData = states[entityConfig.entity];
  const friendlyName = stateData?.attributes?.friendly_name;
  return friendlyName;
};

const getSecondaryInfo = (entityConfig) => {
  // https://www.home-assistant.io/dashboards/entities/#secondary_info
  const stateData = states[entityConfig.entity];

  if (entityConfig.secondaryInfo) {
    if (entityConfig.secondaryInfo.startsWith('attribute.')) {
      const attribute = entityConfig.secondaryInfo.replace('attribute.', '');
      if (stateData?.attributes[attribute]) {
        return stateData.attributes[attribute];
      } else {
        return '?';
      }
    } else if (entityConfig.secondaryInfo.startsWith('sensor.')) {
      const stateData = states[entityConfig.secondaryInfo];
      const state = stateData.state;
      const unitOfMeasurement = stateData?.attributes?.unit_of_measurement;
      return unitOfMeasurement ? `${state} ${unitOfMeasurement}` : state;
    }
  }

  switch (entityConfig.secondaryInfo) {
    case 'last-changed':
      return `${formatDistance(new Date(), parseISO(stateData.lastChanged))} ${t(
        'datetime.ago'
      )}`;
    case 'last-updated':
      return `${formatDistance(new Date(), parseISO(stateData.lastUpdated))} ${t(
        'datetime.ago'
      )}`;
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

const getGroupEntities = (groupConfig) => {
  return props.entities.filter((entity) => entity.group === groupConfig.id);
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
            <span class="mdi text-light text-lg" :class="getIcon(entityConfig)" />
          </span>
          <span class="flex flex-col">
            <span class="font-medium">
              {{ getName(entityConfig) }}
            </span>
            <span class="text-sm text-light">
              {{ getSecondaryInfo(entityConfig) }}
            </span>
          </span>
          <span class="flex-grow text-right font-semibold">
            {{ getValue(entityConfig) }}
          </span>
        </div>
      </template>
    </div>
  </template>

  <template v-else-if="display === 'grid'">
    <div :class="['grid', `grid-cols-${columns}`, 'gap-4']">
      <template
        v-for="(entityConfig, index) in entities"
        :key="`${entityConfig.entity}_${index}`"
      >
        <div v-if="entityConfig.entity in states" class="d-stat inline p-0">
          <div class="d-stat-title leading-4 opacity-100 text-sm font-medium">
            <span class="mdi text-light mr-1" :class="getIcon(entityConfig)" />
            <span class="text-light">{{ getName(entityConfig) }}</span>
          </div>
          <div class="d-stat-value px-1 text-lg font-semibold">
            {{ getValue(entityConfig) }}
          </div>
          <div class="d-stat-desc leading-4 px-1 text-sm text-light opacity-100">
            {{ getSecondaryInfo(entityConfig) }}
          </div>
        </div>
      </template>
    </div>
  </template>

  <template v-else-if="display === 'grouped' && groups.length">
    <div class="flex flex-col gap-2">
      <template v-for="(groupConfig, index) in groups" :key="`group_${index}`">
        <div class="flex gap-3 items-center text-sm">
          <span>
            <span
              v-if="groupConfig.icon"
              class="mdi text-light text-xl"
              :class="`mdi-${groupConfig.icon}`"
            />
          </span>
          <span v-if="groupConfig.title" class="flex flex-col">
            <span class="font-medium">
              {{ groupConfig.title }}
            </span>
          </span>
          <div class="flex-grow flex gap-4 justify-end">
            <template
              v-for="(entityConfig, entityIndex) in getGroupEntities(groupConfig)"
              :key="`${index}_${entityConfig.entity}_${entityIndex}`"
            >
              <div
                v-if="entityConfig.entity in states"
                class="d-stat inline p-0 w-fit text-center"
              >
                <div
                  v-if="getName(entityConfig)"
                  class="d-stat-title leading-4 opacity-100 text-sm font-medium"
                >
                  <span class="text-light">{{ getName(entityConfig) }}</span>
                </div>
                <div class="d-stat-value px-1 text-lg font-semibold">
                  {{ getValue(entityConfig) }}
                </div>
              </div>
            </template>
          </div>
        </div>
      </template>
    </div>
  </template>
</template>
