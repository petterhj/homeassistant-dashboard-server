import { reactive, toRefs } from 'vue';
import { ValidationError } from '@/util/errors';

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
      const response = await fetch('/api/config');

      if (!response?.ok) {
        if (response.status === 422) {
          const data = await response.json();
          throw new ValidationError('Configuration error', data?.detail);
        }
        state.error = new Error(`Server connection error (${response.status})`);
        return;
      }

      try {
        const data = await response.json();
        state.config = data;
      } catch (error) {
        throw new Error(`Received invalid JSON response from ${response.url}`);
      }
    } catch (error) {
      state.error = error;
      return;
    }

    return state.config;
  };

  return { ...toRefs(state), getConfig };
}
