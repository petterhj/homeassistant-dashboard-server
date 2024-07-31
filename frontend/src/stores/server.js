import { reactive, toRefs } from 'vue';
import { ValidationError } from '@/util/errors';

const state = reactive({
  config: null,
});

export function useServer() {
  const getConfig = async () => {
    if (state.config) {
      return state.config;
    }

    console.warn('Fetching dashboard config...');

    const response = await fetch('/api/config');

    console.debug(
      `Request: ${response.url}, status=${response.status}, ok=${response.ok}`
    );

    if (!response?.ok) {
      if (response.status === 422) {
        const data = await response.json();
        throw new ValidationError('Configuration error', data?.detail);
      }
      throw new Error(`Server connection error (${response.status})`);
    }

    try {
      const data = await response.json();
      state.config = data;
    } catch {
      throw new Error(`Received invalid JSON response from ${response.url}`);
    }

    return state.config;
  };

  return { ...toRefs(state), getConfig };
}
