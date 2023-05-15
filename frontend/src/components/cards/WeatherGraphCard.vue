<script setup>
import { computed } from 'vue';
import { add, sub, parseISO, endOfDay, startOfDay, eachHourOfInterval } from 'date-fns';
import { Line } from 'vue-chartjs';
import { cssvar } from '@/util/layout';
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
  borderColor: cssvar('--color-dark-rgb'),
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
          borderColor: cssvar('--color-dark-rgb'),
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
  const historyData = history ? history : [];

  const temperatureData = historyData
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
        borderColor: cssvar('--color-dark-rgb'),
        backgroundColor: cssvar('--color-lightest-rgb'),
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

const chartProps = computed(() => {
  let options = chart.options;
  const values = chartData.value?.datasets[0].data;

  if (values.length) {
    const min = Math.min(...values.map((v) => v.y));
    const max = Math.max(...values.map((v) => v.y));

    options.scales.y.min = Math.floor(min - min * 0.15);
    options.scales.y.max = Math.ceil(max * 1.15);
  }

  return {
    options,
    data: chartData.value,
  };
});
</script>

<template>
  <Line v-if="chartData" v-bind="chartProps" />
</template>
