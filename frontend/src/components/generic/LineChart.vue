<script setup>
import { computed, ref } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import {
  GridComponent,
  MarkLineComponent,
  MarkPointComponent,
  TitleComponent,
  TooltipComponent,
} from 'echarts/components';
import { LabelLayout } from 'echarts/features';
import { format } from 'date-fns';
import VChart from 'vue-echarts';
import { cssvar } from '@/util/layout';
import { DEFAULT_LABEL_STYLE } from '@/util/chart';

use([
  CanvasRenderer,
  GridComponent,
  LabelLayout,
  LineChart,
  MarkLineComponent,
  MarkPointComponent,
  TitleComponent,
  TooltipComponent,
]);

const chart = ref(null);

const props = defineProps({
  data: {
    type: Array,
    required: false,
    default: () => [],
  },
  xAxis: {
    type: Boolean,
    required: false,
    default: true,
  },
  xFormat: {
    type: String,
    required: false,
    default: null,
  },
  xAxisScale: {
    type: Object,
    required: false,
    default: () => {
      // min, max, minInterval, maxInterval
    },
  },
  yAxis: {
    type: Boolean,
    required: false,
    default: true,
  },
  yAxisScale: {
    type: Object,
    required: false,
    default: () => {
      // min, max, minInterval, maxInterval
    },
  },
  yValueFormatter: {
    type: Function,
    required: false,
    default: null,
  },
  lineSymbols: {
    type: Boolean,
    required: false,
    default: true,
  },
  labels: {
    type: [Boolean, Array],
    required: false,
    default: true,
  },
  stepLine: {
    type: Boolean,
    required: false,
    default: false,
  },
  seriesZIndex: {
    type: Number,
    required: false,
    default: null,
  },
  annotations: {
    type: Array,
    required: false,
    default: () => [],
  },
});

defineEmits(['finished']);

const markPointData = computed(() => {
  const data = [];
  if (props.labels?.length) {
    if (props.labels.includes('min')) {
      data.push({ type: 'min' });
    }
    if (props.labels.includes('max')) {
      data.push({ type: 'max' });
    }
  }
  return data;
});

const chartOptions = computed(() => {
  return {
    animation: false,
    grid: {
      top: 15,
      bottom: 15,
      left: props.yAxis ? 15 : 0,
      right: props.yAxis ? 15 : 0,
      containLabel: true,
    },
    tooltip: {
      trigger: 'item',
      formatter: ({ data }) => {
        try {
          const [x, y] = data;
          return `<div>${format(x, 'yy-MM-dd, HH:mm x')}: ${y}</div>`;
        } catch {
          /* pass */
        }
      },
    },
    xAxis: {
      show: true,
      type: 'time',
      ...props.xAxisScale,
      splitLine: { show: false },
      axisLine: {
        show: props.xAxis,
        lineStyle: { width: 2 },
      },
      axisTick: { show: false },
      axisLabel: {
        show: props.xAxis,
        formatter: props.xFormat
          ? (value) => {
            return format(value, props.xFormat);
          }
          : {
            year: '{yyyy}',
            month: '{MMM}',
            day: '{d} {MMM}',
            hour: '{HH}:{mm}',
            minute: '{HH}:{mm}',
            second: '{HH}:{mm}:{ss}',
            millisecond: '{hh}:{mm}:{ss} {SSS}',
            none: '{yyyy}-{MM}-{dd} {hh}:{mm}:{ss} {SSS}',
          },
        fontSize: 12,
        fontWeight: 'bolder',
        hideOverlap: true,
        lineHeight: 24,
      },
    },
    yAxis: {
      show: true,
      type: 'value',
      scale: 'value',
      ...props.yAxisScale,
      splitLine: { show: false },
      axisLabel: {
        show: props.yAxis,
        formatter: (value) => {
          return props.yValueFormatter ? props.yValueFormatter(value) : value;
        },
        fontSize: 12,
        fontWeight: 'bolder',
        hideOverlap: true,
        lineHeight: 24,
      },
    },
    series: props.data.map((s) => ({
      type: 'line',
      smooth: true,
      step: props.stepLine,
      sampling: 'lttb',
      showSymbol: true,
      symbolSize: props.lineSymbols ? 6 : 0,
      color: cssvar('--color-dark-rgb'),
      areaStyle: { opacity: 0.25 },
      z: props.seriesZIndex,
      emphasis: { disabled: true },
      lineStyle: { width: 4 },
      label: {
        show: props.labels === true,
        formatter: ({ data }) => {
          // eslint-disable-next-line no-unused-vars
          const [x, y] = data;
          return props.yValueFormatter ? props.yValueFormatter(y) : y;
        },
        ...DEFAULT_LABEL_STYLE,
      },
      labelLayout: { hideOverlap: true },
      markLine: {
        data: props.annotations,
        silent: true,
        symbol: ['none', 'none'],
        label: { show: false },
        lineStyle: {
          width: 2,
          color: cssvar('--color-dark-rgb'),
        },
      },
      markPoint: {
        symbol: 'rect',
        symbolSize: 0,
        data: markPointData.value,
        label: {
          show: true,
          formatter: ({ value }) => {
            return props.yValueFormatter ? props.yValueFormatter(value) : value;
          },
          ...DEFAULT_LABEL_STYLE,
        },
      },
      data: s,
    })),
  };
});
</script>

<template>
  <v-chart
    ref="chart"
    :option="chartOptions"
    autoresize
    @finished="$emit('finished')"
  />
</template>
