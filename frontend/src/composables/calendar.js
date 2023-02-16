import { reactive } from 'vue';

export function useCalendar(config) {
  const calendar = reactive({
    events: [],
    error: null,
  });

  console.log('Fetching calendar data');

  fetch('/ha/calendar')
    .then((res) => res.json())
    .then((json) => {
      if (json.detail) {
        console.error(json.detail);
        calendar.error = json.detail;
        return;
      }

      calendar.events = json;
    })
    .catch((err) => {
      console.error('Could not fetch calendar data', err);
      calendar.error = err;
    });

  return calendar;
}
