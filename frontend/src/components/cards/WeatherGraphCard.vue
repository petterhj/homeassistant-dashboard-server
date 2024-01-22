<script setup>
import { computed } from 'vue';
import { add, sub, parseISO } from 'date-fns';
import { useI18n } from 'vue-i18n';
import { useHomeAssistant } from '@/stores/homeassistant';
import { useCard } from '@/composables/card';
import { BASE_CARD_PROPS } from '@/util/card';
import { parseAnnotations } from '@/util/chart';
import BaseCard from '@/components/generic/BaseCard.vue';
import LineChart from '@/components/generic/LineChart.vue';

const { t } = useI18n();
const { getEntity, getServiceResponse } = useHomeAssistant();

const props = defineProps({
  ...BASE_CARD_PROPS,
  entity: {
    type: String,
    required: true,
  },
  attribute: {
    type: String,
    required: false,
    default: 'temperature',
  },
  unit: {
    type: String,
    required: false,
    default: null,
  },
  includeForecast: {
    type: Boolean,
    required: false,
    default: true,
  },
  includeHistory: {
    type: Boolean,
    required: false,
    default: true,
  },
  forecastType: {
    type: String,
    required: false,
    default: 'hourly',
    validator(value) {
      return ['daily', 'hourly', 'twice_daily'].includes(value);
    },
  },
  annotations: {
    type: Array,
    required: false,
    default: () => ['now', 'startOfDay', 'endOfDay'],
  },
});
const card = useCard(props, {
  title: t('weather.forecast'),
  icon: 'chart-timeline-variant',
  style: ['h-56'],
});

const entity = await getEntity(props.entity, { history: props.includeHistory });
const forecast = props.includeForecast
  ? await getServiceResponse('weather', 'get_forecasts', props.entity, {
      type: props.forecastType,
    })
  : null;

const unit = props.unit || entity?.attributes[`${props.attribute}_unit`];

const chartData = computed(() => {
  const { attributes, history, lastUpdated } = entity;
  let data = [[parseISO(lastUpdated), attributes[props.attribute]]];
  if (props.includeHistory && history) {
    data = data.concat(
      history.map((f) => [parseISO(f.last_updated), f.attributes[props.attribute]])
    );
  }

  if (props.includeForecast && forecast) {
    const forecastData = forecast?.forecast || [];
    data = data.concat(
      forecastData.map((f) => [parseISO(f.datetime), f[props.attribute]])
    );
  }

  return [data.sort((a, b) => a[0] - b[0])];
});

const xAxisScale = computed(() => {
  const now = new Date();
  return {
    min: sub(now, { hours: 12 }),
    max: add(now, { hours: 24 }),
  };
});

const yAxisScale = computed(() => {
  const { min: xMin, max: xMax } = xAxisScale.value;

  if (xMin && xMax && chartData.value.length) {
    const values = chartData.value
      .map((s) => s.filter((p) => p[0] >= xMin && p[0] <= xMax).map((p) => p[1]))
      .flat();
    return {
      min: Math.floor(Math.min(...values)) + -2,
      max: Math.ceil(Math.max(...values)) + 2,
    };
  }
  return {
    minInterval: 1,
    maxInterval: 1,
    min: 'dataMin',
    max: 'dataMax',
    boundaryGap: ['10%', '10%'],
  };
});

const chartProps = computed(() => {
  return {
    data: chartData.value,
    xFormat: 'HH',
    xAxis: false,
    xAxisScale: xAxisScale.value,
    yAxis: false,
    yAxisScale: yAxisScale.value,
    yValueFormatter: (val) => (unit ? `${val}${unit}` : val),
    stepLine: false,
    annotations: parseAnnotations(props.annotations, chartData.value),
  };
});
</script>

<template>
  <BaseCard v-bind="card">
    <LineChart v-bind="chartProps" />
  </BaseCard>
</template>
