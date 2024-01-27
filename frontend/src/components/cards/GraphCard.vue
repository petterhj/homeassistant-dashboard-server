<script setup>
import { computed } from 'vue';
import { parseISO } from 'date-fns';
import { LTTB } from 'downsample';
import { useHomeAssistant } from '@/stores/homeassistant';
import { useCard } from '@/composables/card';
import { BASE_CARD_PROPS } from '@/util/card';
import { parseAnnotations } from '@/util/chart';
import BaseCard from '@/components/generic/BaseCard.vue';
import LineChart from '@/components/generic/LineChart.vue';

const { getEntities } = useHomeAssistant();

const props = defineProps({
  ...BASE_CARD_PROPS,
  entities: {
    type: Array,
    required: true,
  },
  unit: {
    type: String,
    required: false,
    default: null,
  },
  labels: {
    type: [Boolean, Array],
    required: false,
    default: () => ['min', 'max'],
  },
  annotations: {
    type: Array,
    required: false,
    default: () => ['now', 'startOfDay', 'endOfDay'],
  },
  xAxis: {
    type: [Boolean, Object],
    required: false,
    default: () => {},
  },
  yAxis: {
    type: [Boolean, Object],
    required: false,
    default: () => {},
  },
  targetResolution: {
    type: Number,
    required: false,
    default: null,
  },
});

const entities = await getEntities(props.entities, { history: true });
const card = useCard(props, { style: ['h-56'] });

const chartData = computed(() => {
  const series = [];
  for (const entity of Object.values(entities)) {
    const { state, history, lastUpdated } = entity;
    let data = [[parseISO(lastUpdated), parseFloat(state)]];
    data = data
      .concat(history.map((r) => [parseISO(r.last_updated), parseFloat(r.state)]))
      .filter((p) => !isNaN(p[1]))
      .sort((a, b) => a[0] - b[0]);

    if (props.targetResolution && props.targetResolution < data.length) {
      data = LTTB(data, 15);
    }

    series.push(data);
  }
  return series;
});

const chartProps = computed(() => {
  return {
    data: chartData.value,
    xAxis: props.xAxis !== false,
    xAxisScale:
      props.xAxis !== false
        ? {
            min: props.xAxis?.min,
            max: props.xAxis?.max,
          }
        : null,
    xFormat: 'HH',
    yAxis: props.yAxis !== false,
    yAxisScale:
      props.yAxis !== false
        ? {
            min: props.yAxis?.min,
            max: props.yAxis?.max,
          }
        : null,
    lineSymbols: false,
    // yValueFormatter: (val) => (unit.value ? `${val} ${unit.value}` : val),
    labels: props.labels,
    annotations: parseAnnotations(props.annotations, chartData.value),
  };
});
</script>

<template>
  <BaseCard v-bind="card">
    <LineChart v-bind="chartProps" />
  </BaseCard>
</template>

<style scoped>
:deep(.card-content) {
  height: 100%;
}
</style>
