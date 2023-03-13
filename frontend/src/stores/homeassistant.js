import { reactive, toRefs } from 'vue';

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
      `/ha/entity/${entityId}?` + new URLSearchParams({ history: fetchHistory })
    );

    console.debug('Request:', response.url);
    console.debug('> Ok:', response.ok);
    console.debug('> Status:', response.status);

    if (!response?.ok) {
      if (response.status === 404) {
        throw new Error(`Entity ${entityId} not found`);
      }
      if (response.status === 422) {
        const data = await response.json();
        console.debug(
          '> Response:',
          data.detail.map((error) => `${error.location}: ${error.message}`)
        );
        throw new Error(
          `Validation error: ${data.detail
            .map((error) => `${error.location}: ${error.message}`)
            .join('\n')}`
        );
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

    const response = await fetch('/ha/calendar');
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
