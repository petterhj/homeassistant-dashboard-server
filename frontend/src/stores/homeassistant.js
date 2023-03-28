import { reactive, toRefs } from 'vue';
import { ValidationError } from '@/util/errors';

const state = reactive({
  entities: {},
  events: [],
});

export function useHomeAssistant() {
  const getEntity = async (entityId, options) => {
    if (Object.prototype.hasOwnProperty.call(state.entities, entityId)) {
      console.debug(`Returning cached entity state for ${entityId}`);
      return state.entities[entityId];
    }

    const fetchHistory = !!options?.history;

    console.warn(`Fetching entity state for ${entityId}, history=${fetchHistory}`);

    const response = await fetch(
      `/api/ha/entity/${entityId}?` + new URLSearchParams({ history: fetchHistory })
    );

    console.debug(
      `Request: ${response.url}, status=${response.status}, ok=${response.ok}`
    );

    if (!response?.ok) {
      if (response.status === 401) {
        const data = await response.json();
        throw new Error(data.detail);
      }
      if (response.status === 404) {
        throw new Error(`Entity ${entityId} not found`);
      }
      if (response.status === 422) {
        const data = await response.json();
        throw new ValidationError('Configuration error', data?.detail);
      }
      if (response.status === 502) {
        throw new Error(`Could not connect to Home Assistant`);
      }
      throw new Error('Could not get entity');
    }

    const data = await response.json();

    if (data.detail) {
      throw new Error(data.detail);
    }

    state.entities[entityId] = {
      id: data.entity_id,
      state: data.state,
      attributes: data.attributes,
      history: data.history,
      lastChanged: data.last_changed,
      lastUpdated: data.last_updated,
    };

    return state.entities[entityId];
  };

  const getEntities = async (entityIds, options) => {
    const entities = {};

    for (const entityId of entityIds) {
      entities[entityId] = await getEntity(entityId, options);
    }

    return entities;
  };

  const getCalendar = async () => {
    console.warn('Fetching calendar data');

    const response = await fetch('/api/ha/calendar');
    const data = await response.json();

    state.events = data;

    return state.events;
  };

  return {
    ...toRefs(state),
    getEntity,
    getEntities,
    getCalendar,
  };
}
