import { createI18n } from 'vue-i18n';

const messages = {
  en: {
    general: {
      loading: 'Loading',
      type: 'Type',
      dashboardError: 'Could not load dashboard',
      noConfiguration: 'No configuration',
      noData: 'No data',
      pageNotFound: 'Page not found',
    },
    datetime: {
      now: 'Now',
      ago: 'ago',
      today: 'Today',
    },
    weather: {
      forecast: 'Forecast',
      states: {
        'clear-night': 'Klart',
        'cloudy': 'Cloudy',
        'fog': 'Fog',
        'hail': 'Hail',
        'lightning-rainy': 'Lightning/rainy',
        'lightning': 'Lightning',
        'partlycloudy': 'Partly cloudy',
        'pouring': 'Pouring',
        'rainy': 'Rainy',
        'snowy-rainy': 'Snowy/rainy',
        'snowy': 'Snowy',
        'sunny': 'Sunny',
        'windy-variant': 'Windy',
        'windy': 'Windy',
      },
    },
    sun: {
      sun: 'Sun',
      sunrise: 'Sunrise',
      sunset: 'Sunset',
      dawn: 'Dawn',
      dusk: 'Dusk',
      solarNoon: 'Solar noon',
    },
    todo: {
      todo: 'Todo',
    },
    petcare: {
      hub: 'Hub',
      flap: 'Flap',
      inside: 'Inside',
      outside: 'Outside',
    },
  },
  nb: {
    general: {
      loading: 'Laster inn',
      type: 'Type',
      dashboardError: 'Kunne ikke laste inn dashbord',
      noConfiguration: 'Mangler konfiguration',
      noData: 'Mangler data',
      pageNotFound: 'Siden finnes ikke',
    },
    datetime: {
      now: 'Nå',
      ago: 'siden',
      today: 'I dag',
    },
    weather: {
      forecast: 'Værvarsel',
      states: {
        'clear-night': 'Klart',
        'cloudy': 'Skyet',
        'fog': 'Tåke',
        'hail': 'Hagl',
        'lightning-rainy': 'Lyn og regn',
        'lightning': 'Lyn',
        'partlycloudy': 'Delvis skyet',
        'pouring': 'Kraftig nedbør',
        'rainy': 'Regn',
        'snowy-rainy': 'Sludd',
        'snowy': 'Snø',
        'sunny': 'Solfylt',
        'windy-variant': 'Vind',
        'windy': 'Vind',
      },
    },
    sun: {
      sun: 'Sol',
      sunrise: 'Soloppgang',
      sunset: 'Solnedgang',
      dawn: 'Gryning',
      dusk: 'Skumring',
      solarNoon: 'Middag',
    },
    todo: {
      todo: 'Gjøreliste',
    },
    petcare: {
      hub: 'Hub',
      flap: 'Flap',
      inside: 'Inne',
      outside: 'Ute',
    },
  },
};

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages,
});

export default i18n;
