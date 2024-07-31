<script setup>
import { computed } from 'vue';
import {
  differenceInSeconds,
  format,
  isBefore,
  isThisWeek,
  isToday,
  parseISO,
  subHours,
} from 'date-fns';
import { useI18n } from 'vue-i18n';
import { useHomeAssistant } from '@/stores/homeassistant';
import { useCard } from '@/composables/card';
import { BASE_CARD_PROPS } from '@/util/card';
import BaseCard from '@/components/generic/BaseCard.vue';

const { t } = useI18n();
const { getCalendar } = useHomeAssistant();

const props = defineProps({
  ...BASE_CARD_PROPS,
  limit: {
    type: Number,
    required: false,
    default: 10,
  },
  calendars: {
    type: Array,
    required: false,
    default: () => [],
  },
});

const events = await getCalendar(props.calendars);
const card = useCard(props, {
  title: 'Calendar',
  icon: 'calendar-blank-outline',
});

const eventDateTime = (event) => {
  // Date format
  const { start, end } = event;

  let dateFormat = format(start, 'EEEEEE. d/M');
  let startTime = format(start, 'HH:mm');
  let endTime = end ? format(end, 'HH:mm') : null;

  if (isToday(start)) {
    dateFormat = t('datetime.today');
  } else if (isThisWeek(start)) {
    dateFormat = format(start, 'iii.');
  }
  dateFormat = dateFormat.charAt(0).toUpperCase() + dateFormat.slice(1);

  if (differenceInSeconds(end, start) === 86400) {
    // All-day event
    return dateFormat;
  } else if (startTime === '00:00' && endTime === '00:00') {
    // Multi-day event
    return `${dateFormat} - ${format(subHours(end, 5), 'iii. d/M')}`;
  }

  return dateFormat + ', ' + startTime + (endTime ? `-${endTime}` : '');
};

const sortedEvents = computed(() => {
  const now = new Date();
  return events
    .map((e) => ({
      ...e,
      start: parseISO(e.start),
      end: parseISO(e.end),
    }))
    .filter((e) => {
      const calendarConfig = props.calendars
        .find((c) => c.entity === e.entity_id);
      if (calendarConfig?.filterBegun === true) {
        return !isBefore(e.start, now);
      }
      return true;
    })
    .sort((a, b) => a.start - b.start)
    .slice(0, props.limit);
});

function eventIcon(event) {
  const calendarConfig = props.calendars
    .find((c) => c.entity === event.entity_id);

  if (calendarConfig?.icon) {
    return calendarConfig.icon;
  }

  return props.icon || card.icon;
}

function showDescription(event) {
  const calendarConfig = props.calendars
    .find((c) => c.entity === event.entity_id);
  if (!event.description || calendarConfig?.showDescription === false) {
    return false;
  }
  return true;
}

function showCalendarName(event) {
  const calendarConfig = props.calendars
    .find((c) => c.entity === event.entity_id);
  if (!event.calendar_name || calendarConfig?.showCalendarName === false) {
    return false;
  }
  return true;
}
</script>

<template>
  <BaseCard v-bind="card">
    <ul>
      <li
        v-for="(event, index) in sortedEvents"
        :key="index"
        class="flex gap-2 mb-1"
      >
        <span
          v-if="eventIcon(event)"
          :class="['mdi', `mdi-${eventIcon(event)}`, 'text-light']"
        />
        <div class="flex flex-col gap-0.25 w-full">
          <div class="flex justify-between font-medium">
            <span class="text-sm">{{ event.summary }}</span>
            <span class="text-xs text-light whitespace-nowrap">
              {{ eventDateTime(event) }}
            </span>
          </div>
          <span
            v-if="showCalendarName(event)"
            class="mt-1 text-xs text-lighter line-clamp-1"
          >
            {{ event.calendar_name }}
          </span>
          <p
            v-if="showDescription(event)"
            class="mt-1 text-xs text-light line-clamp-2"
          >
            {{ event.description }}
          </p>
        </div>
      </li>
    </ul>
  </BaseCard>
</template>
