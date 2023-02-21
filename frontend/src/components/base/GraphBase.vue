<script setup>
import { ref } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

const props = defineProps({
  series: {
    type: Array,
    required: true,
  },
  options: {
    type: Object,
    required: false,
    default: null,
  },
  type: {
    type: String,
    required: false,
    default: 'area',
  },
});

const options = ref({
  ...{
    chart: { toolbar: { show: false }, height: '100%' },
    legend: { show: false },
    grid: { show: true },
    stroke: { curve: 'smooth' },
    colors: ['#333333'],
    fill: {
      type: 'solid',
      colors: ['#D9D9D9'],
    },
    tooltip: {
      enabled: true,
      marker: { show: true },
      // intersect: true,
      // shared: false,
      fixed: {
        enabled: false,
        position: 'topRight',
        offsetX: 0,
        offsetY: 0,
      },
    },
  },
  ...props.options,
});
</script>

<template>
  <component
    class="-mx-4"
    :is="VueApexCharts"
    :options="options"
    :series="series"
    :type="type"
    :height="'100%'"
  />
</template>
