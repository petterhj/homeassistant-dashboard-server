<script setup>
import { computed, ref, onMounted } from 'vue';
import { format, parseISO, endOfDay, startOfDay, subHours, addHours } from 'date-fns';
import { useI18n } from 'vue-i18n';
import { useHomeAssistant } from '@/stores/homeassistant';

import BaseGraph from '../base/GraphBase.vue';

const { t } = useI18n();
const { getEntityState } = useHomeAssistant();

const props = defineProps({
  entity: {
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

const entity = await getEntityState(props.entity, { history: true });

const options = computed(() => {
  return {
    grid: {
      show: true,
      // padding: {
      //   top: -10,
      //   bottom: 0,
      //   left: 25,
      //   right: 23,
      // },
    },
    xaxis: {
      type: 'datetime',
      min: subHours(new Date(), 22).getTime(),
      max: addHours(new Date(), 22).getTime(),
      // tickAmount: 16,
      tickAmount: 'dataPoints',
      tickPlacement: 'on',
      labels: {
        formatter: (val) => {
          const datetime = new Date(val);
          if (val && !isNaN(datetime)) {
            return format(datetime, 'HH');
          }
        },
      },
      tooltip: {
        enabled: true,
        // formatter: undefined,
        offsetY: -100,
        // style: {
        //   fontSize: 0,
        //   fontFamily: 0,
        // },
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
  if (!entity) {
    return [];
  }

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
  <BaseGraph id="sun-graph" :series="timeSeriesData" :options="options" class="h-64" />
</template>

<style>
#sun-graph .apexcharts-data-labels:nth-child(1) {
  display: none;
}
</style>
