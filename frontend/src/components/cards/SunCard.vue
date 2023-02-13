<script setup>
import { computed } from 'vue';
import { format, endOfDay, startOfDay, addHours, subHours } from 'date-fns';
import { useEntity } from '@/composables/entity.js';

import BaseCard from './BaseCard.vue';
import BaseGraph from '../BaseGraph.vue';

const props = defineProps({
  entityId: {
    type: String,
    required: true,
  },
});

const entity = useEntity(props.entityId, { history: true });

const options = computed(() => {
  return {
    grid: {
      show: false,
      padding: {
        top: -20,
        bottom: -10,
        left: 10,
        right: 23,
      },
    },
    plotOptions: {
      bar: {
        horizontal: true,
        rangeBarGroupRows: true,
      },
    },
    // colors: ['#D9D9D9', '#333'],
    colors: [
      ({ seriesIndex, w }) => {
        const name = w.globals.seriesNames[seriesIndex];
        if (name === 'above_horizon') {
          return '#666666';
        }
        return '#D9D9D9';
      },
    ],
    fill: { type: 'solid' },
    xaxis: {
      type: 'datetime',
      min: subHours(new Date(), 22).getTime(),
      max: addHours(new Date(), 22).getTime(),
      tickAmount: 16,
      tickPlacement: 'on',
      labels: {
        datetimeUTC: false,
        formatter: (val) => {
          // console.log('ts', timestamp, val);
          const datetime = new Date(val);
          if (val && !isNaN(datetime)) {
            return format(datetime, 'HH');
          }
        },
      },
      // axisBorder: { show: false },
      // axisTicks: { show: false },
    },
    yaxis: { show: false },
    dataLabels: {
      // position: 'top',
      enabled: false,
      // textAnchor: 'start',
      // style: {
      //     // fontSize: '10pt',
      //     colors: ['#000']
      // },
      // formatter: function(val, opt) {
      //   // console.log(val, opt)
      //   return opt.w.globals.seriesNames[opt.seriesIndex];
      // },
      // offsetX: 0,
      // horizontal: true,
    },
    annotations: {
      xaxis: [
        {
          x: new Date().getTime(),
          borderColor: '#333',
          borderWidth: 2,
          strokeDashArray: 4,
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

const seriesData = computed(() => {
  const states = entity.history
    .map((entry) => ({
      state: entry.state,
      startTime: new Date(entry.last_changed),
    }))
    .concat([
      {
        state: 'below_horizon',
        startTime: new Date(entity.attributes.next_setting),
      },
      {
        state: 'above_horizon',
        startTime: new Date(entity.attributes.next_rising),
      },
    ])
    .sort(function (a, b) {
      return b.date - a.date
    })
    .map((entry, index, array) => {
      const next = array[index + 1];
      // console.log(index, entry, next);
      return {
        ...entry,
        endTime: next ? next.startTime : null,
      };
    });
  // console.log(JSON.stringify(states, 0, 2));
  return states.map((entry) => ({
    name: entry.state,
    data: [
      {
        x: 'Sun',
        y: [
          entry.startTime.getTime(),
          entry.endTime ? entry.endTime.getTime() : endOfDay(entry.startTime).getTime(),
        ],
      },
    ],
  }));
});
</script>

<template>
  <BaseCard :entity="entity" :height="16">
    <BaseGraph :series="seriesData" :options="options" type="rangeBar" />
  </BaseCard>
</template>
