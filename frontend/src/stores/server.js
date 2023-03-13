import { reactive, toRefs } from 'vue';

const state = reactive({
  config: null,
  error: null,
});

export function useServer() {
  const getConfig = async () => {
    if (state.config) {
      return state.config;
    }

    console.warn('Fetching dashboard config...');

    try {
      const response = await fetch('/config');

      if (!response?.ok) {
        state.error = new Error(`Server connection error (${response.status})`);
        return;
      }
      const data = await response.json();
      state.config = data;
    } catch (error) {
      state.error = error;
      return;
    }

    return state.config;
  };

  return { ...toRefs(state), getConfig };
}
