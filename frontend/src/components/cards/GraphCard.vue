<script setup>
import { computed } from 'vue';
import { add, sub, parseISO, endOfDay, startOfDay, eachHourOfInterval } from 'date-fns';
import { Line } from 'vue-chartjs';
import { useChart } from '@/composables/chart';
import { useHomeAssistant } from '@/stores/homeassistant';

const { getEntity } = useHomeAssistant();

const props = defineProps({
  entity: {
    type: String,
    required: true,
  },
  // attribute: {
  //   type: String,
  //   required: true,
  // },
  show: {
    type: Object,
    required: false,
  },
  dateFormat: {
    type: String,
    required: false,
    default: 'MM yy',
  },
});

const now = new Date();

const annotationBorder = {
  drawTime: 'beforeDatasetsDraw',
  type: 'line',
  borderWidth: 3,
  borderDash: [3, 6],
  borderColor: '#999999',
};

const labels = eachHourOfInterval({
  start: sub(now, { hours: 23 }),
  // end: add(now, { hours: 24 }),
  end: now,
});

const chart = useChart({
  plugins: {
    annotation: {
      annotations: {
        startOfDay: {
          ...annotationBorder,
          xMin: startOfDay(now),
          xMax: startOfDay(now),
        },
        now: {
          ...annotationBorder,
          xMin: new Date(),
          xMax: new Date(),
          borderColor: '#000000',
          borderDash: [0, 0],
        },
        endOfDay: {
          ...annotationBorder,
          xMin: endOfDay(now),
          xMax: endOfDay(now),
        },
      },
    },
  },
  scales: {
    x: {
      min: labels[0],
      max: labels[labels.length - 1],
      ticks: {
        maxRotation: 0,
      },
    },
  },
});

const entity = await getEntity(props.entity, { history: true });

const chartData = computed(() => {
  const { history } = entity;

  const datasetData = history
    .filter((value, index) => {
      return index % 5 == 0;
    })
    .map((entry) => ({
      x: parseISO(entry.last_updated),
      y: entry.state,
    }));

  const data = {
    labels,
    datasets: [
      {
        yAxisID: 'y',
        xAxisID: 'x',
        data: datasetData,
        // data: [],
        borderWidth: 5,
        fill: true,
        pointRadius: 0,
        // https://www.chartjs.org/docs/latest/charts/line.html#line-styling
        borderColor: '#333',
        backgroundColor: '#DFDFDF',
        tension: 0.3,
        datalabels: {
          display: props.show?.labels ? 'auto' : false,
          formatter: (value) => {
            return value.y;
          },
        },
      },
    ],
  };

  return data;
});
</script>

<template>
  <Line v-if="chartData" :options="chart.options" :data="chartData" />
</template>