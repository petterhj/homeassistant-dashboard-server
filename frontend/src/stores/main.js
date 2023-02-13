import { ref } from 'vue';
import { defineStore } from 'pinia';

export const useStore = defineStore('main', () => {
  const apiError = ref(false);

  return { apiError };
});
