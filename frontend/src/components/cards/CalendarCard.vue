<script setup>
import { format, parseISO, differenceInHours } from 'date-fns';
import { useCalendar } from '@/composables/calendar.js';

import BaseCard from './BaseCard.vue';

const props = defineProps({
  title: {
    type: String,
    required: false,
    default: null,
  },
  icon: {
    type: String,
    required: false,
    default: null,
  },
  iconItem: {
    type: String,
    required: false,
    default: null,
  },
  iconItems: {
    type: Object,
    required: false,
    default: null,
  },
});

const calendar = useCalendar();

function eventTime(event) {
  const eventStart = parseISO(event.start);
  const eventEnd = event.end ? parseISO(event.end) : null;
  let formattedEnd = eventEnd ? format(eventEnd, '-HH:mm') : null;
  const formattedDate = format(eventStart, 'HH:mm');
  return formattedDate + formattedEnd;
}

function eventIcon(event) {
  if (
    props.iconItems &&
    Object.prototype.hasOwnProperty.call(props.iconItems, event.entity_id)
  ) {
    return props.iconItems[event.entity_id];
  }
  return props.iconItem || props.icon;
}
</script>

<template>
  <BaseCard :error="calendar.error" :title="title" :icon="icon">
    <ul>
      <li
        v-for="(event, index) in calendar.events"
        :key="index"
        class="flex gap-2 ml-2 mb-2"
      >
        <span
          v-if="iconItems || iconItem || icon"
          :class="['mdi', `mdi-${eventIcon(event)}`, 'text-gray-400']"
        />
        <div class="flex flex-col gap-0.25">
          <div class="flex justify-between font-medium">
            <span class="text-sm">{{ event.summary }}</span>
            <span class="text-xs text-gray-500">
              {{ format(parseISO(event.start), 'EEEEEE. d/M') }}
            </span>
          </div>
          <div class="flex justify-between text-sm text-gray-500">
            <span class="text-xs">{{ event.calendar_name }}</span>
            <span class="text-xs">{{ eventTime(event) }}</span>
          </div>
          <p
            v-if="event.description"
            class="mt-1 text-xs text-gray-500 font-light line-clamp-2"
          >
            {{ event.description }}
          </p>
        </div>
      </li>
    </ul>
  </BaseCard>
</template>
