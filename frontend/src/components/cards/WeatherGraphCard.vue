<script setup>
import { computed } from 'vue';
import { format, parseISO, endOfDay, startOfDay, subHours, addHours } from 'date-fns';
import { useI18n } from 'vue-i18n';
import { useEntity } from '@/composables/entity.js';

import BaseCard from './BaseCard.vue';
import BaseGraph from '../BaseGraph.vue';

const props = defineProps({
  entityId: {
    type: String,
    required: true,
  },
  attribute: {
    type: String,
    required: true,
  },
  dateFormat: {
    type: String,
    required: false,
    default: 'MM yy',
  },
});

const { t } = useI18n();
const entity = useEntity(props.entityId, { history: true });

const options = computed(() => {
  return {
    grid: {
      show: false,
      padding: {
        top: -10,
        bottom: 0,
        left: 25,
        right: 23,
      },
    },
    xaxis: {
      type: 'datetime',
      min: subHours(new Date(), 22).getTime(),
      max: addHours(new Date(), 22).getTime(),
      tickAmount: 16,
      tickPlacement: 'on',
      labels: {
        formatter: (val) => {
          const datetime = new Date(val);
          if (val && !isNaN(datetime)) {
            return format(datetime, 'HH');
          }
        },
      },
    },
    yaxis: { show: false },
    dataLabels: {
      enabled: true,
      style: {
        fontFamily: 'Roboto',
        fontWeight: 'bold',
        colors: ['#666'],
      },
      background: {
        foreColor: '#FFFFFF',
        borderWidth: 0,
        padding: 1,
      },
    },
    annotations: {
      xaxis: [
        {
          x: new Date().getTime(),
          borderColor: '#333',
          borderWidth: 2,
          strokeDashArray: 4,
          label: {
            text: t('datetime.now'),
            orientation: 'horizontal',
            borderColor: 'transparent',
            style: {
              color: '#000',
              background: '#EFEFEF',
            },
          },
        },
        {
          x: startOfDay(new Date()).getTime(),
          borderColor: '#333',
        },
        {
          x: endOfDay(new Date()).getTime(),
          borderColor: '#333',
        },
      ],
    },
  };
});

const timeSeriesData = computed(() => {
  const history = entity.history.map((measurement) => ({
    x: parseISO(measurement.last_changed).getTime(),
    y: measurement.attributes[props.attribute],
  }));
  const forecast = entity.attributes?.forecast
    ? entity.attributes.forecast.map((measurement) => ({
        x: parseISO(measurement.datetime).getTime(),
        y: measurement[props.attribute],
      }))
    : [];
  return [
    {
      name: entity.id,
      data: history.concat(forecast),
    },
  ];
});
</script>

<template>
  <BaseCard :entity="entity" class="h-48">
    <BaseGraph id="sun-graph" :series="timeSeriesData" :options="options" class="h-48" />
  </BaseCard>
</template>

<style>
#sun-graph .apexcharts-data-labels:nth-child(1) {
  display: none;
}
</style>
