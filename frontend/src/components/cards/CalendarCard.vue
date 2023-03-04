<script setup>
import { format, parseISO, isThisWeek } from 'date-fns';
import { useHomeAssistant } from '@/stores/homeassistant';
import CardTitle from './partials/CardTitle.vue';

const { getCalendar } = useHomeAssistant();

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
  itemIcon: {
    type: String,
    required: false,
    default: null,
  },
  calendarIcons: {
    type: Object,
    required: false,
    default: null,
  },
});

const events = await getCalendar();

const eventDate = (event) => {
  const eventStart = parseISO(event.start);
  if (isThisWeek(eventStart)) {
    return format(eventStart, 'EEEE');
  }
  return format(eventStart, 'EEEEEE. d/M');
};
const eventTime = (event) => {
  const eventStart = parseISO(event.start);
  const eventEnd = event.end ? parseISO(event.end) : null;
  let formattedEnd = eventEnd ? format(eventEnd, '-HH:mm') : null;
  const formattedDate = format(eventStart, 'HH:mm');
  return formattedDate + formattedEnd;
};
const eventIcon = (event) => {
  if (
    props.calendarIcons &&
    Object.prototype.hasOwnProperty.call(props.calendarIcons, event.entity_id)
  ) {
    return props.calendarIcons[event.entity_id];
  }
  return props.itemIcon || props.icon;
};
</script>

<template>
  <CardTitle :title="title" :icon="icon" />

  <ul>
    <li v-for="(event, index) in events" :key="index" class="flex gap-2 ml-2 mb-2">
      <span
        v-if="calendarIcons || itemIcons || icon"
        :class="['mdi', `mdi-${eventIcon(event)}`, 'text-gray-400']"
      />
      <div class="flex flex-col gap-0.25 w-full">
        <div class="flex justify-between font-medium">
          <span class="text-sm">{{ event.summary }}</span>
          <span class="text-xs text-gray-500 whitespace-nowrap">
            {{ eventDate(event) }}
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
</template>
