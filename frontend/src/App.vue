<script setup>
import { format } from 'date-fns';
import { RouterView } from 'vue-router';
import { useServer } from '@/stores/server';

const { config, currentView } = useServer();
</script>

<template>
  <div :class="['h-screen flex flex-col', config.container?.style]">
    <main :class="config.container.show_footer ? 'h-[calc(100%-2rem)]' : 'h-full'">
      <div :class="['h-full flex flex-col gap-4 p-4 pb-0', currentView?.style]">
        <RouterView />
      </div>
    </main>

    <footer
      v-if="config.container.show_footer"
      class="flex flex-row justify-between items-center h-8 px-4 leading-8"
    >
      <div class="text-sm">
        <span class="mdi mdi-refresh text-lighter mr-2" />
        <span class="text-dark font-medium">
          {{ format(new Date(), 'dd.MM.yy - HH:mm') }}
        </span>
      </div>

      <div class="text-xs text-lightest mr-2">
        <span v-if="currentView?.name">{{ currentView?.name }} @ </span>
        <span>{{ config?.version || 'dev' }}</span>
      </div>
    </footer>
  </div>
</template>
