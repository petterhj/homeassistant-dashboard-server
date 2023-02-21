import { reactive, toRefs } from 'vue';

const state = reactive({
  dashboard: null,
});

console.log('Fetching dashboard config...');
const response = await fetch(`/proxy/config/`);
const data = await response.json();
state.dashboard = data.dashboard;

export function useDashboard() {
  return { ...toRefs(state) };
}
