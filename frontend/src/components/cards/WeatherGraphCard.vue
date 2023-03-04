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
  attribute: {
    type: String,
    required: true,
  },
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
  start: sub(now, { hours: 12 }),
  end: add(now, { hours: 24 }),
});

const chart = useChart({
  plugins: {
    datalabels: {
      display: !!props.show?.labels,
    },
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
  const { attributes, history } = entity;

  const temperatureData = history
    .map((f) => ({
      x: parseISO(f.last_updated),
      y: f.attributes.temperature,
    }))
    .concat(
      attributes.forecast.map((f) => ({
        x: parseISO(f.datetime),
        y: f.temperature,
      }))
    );

  const data = {
    labels,
    datasets: [
      {
        yAxisID: 'y',
        xAxisID: 'x',
        data: temperatureData,
        // data: [],
        borderWidth: 5,
        fill: true,
        pointRadius: 0,
        // https://www.chartjs.org/docs/latest/charts/line.html#line-styling
        borderColor: '#333',
        backgroundColor: '#DFDFDF',
        tension: 0.3,
        datalabels: {
          display: 'auto',
          formatter: (value) => {
            return value.y + '°';
          },
        },
      },
      // { data: windSpeedData },
    ],
  };

  return data;
});
</script>

<template>
  <Line v-if="chartData" :options="chart.options" :data="chartData" />
</template>
