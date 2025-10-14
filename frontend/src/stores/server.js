import { reactive, toRefs, computed } from 'vue';
import { useRoute } from 'vue-router';
import { ValidationError } from '@/util/errors';

const state = reactive({
  config: null,
});

export function useServer() {
  const route = useRoute();

  const getConfig = async () => {
    if (state.config) {
      return state.config;
    }

    console.info('Fetching dashboard config...');

    const response = await fetch('/api/config');

    console.info(
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

  const currentView = computed(() => {
    if (!state.config || !route.params.viewName) {
      return null;
    }
    
    return state.config.views?.find(view => view.name === route.params.viewName) || null;
  });

  return { ...toRefs(state), getConfig, currentView };
}
