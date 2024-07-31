import { reactive, toRefs } from 'vue';
import { ValidationError } from '@/util/errors';

const state = reactive({
  entities: {},
  events: [],
});

export function useHomeAssistant() {
  const getEntity = async (entityId, options) => {
    if (Object.prototype.hasOwnProperty.call(state.entities, entityId)) {
      const entityState = state.entities[entityId];
      if (options?.history === true && !entityState.history) {
        console.warn(`Refetching entity state for ${entityId} (missing history)`);
      } else {
        console.warn(`Returning cached entity state for ${entityId}`);
        return entityState;
      }
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
        throw new Error('Could not connect to Home Assistant');
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

  const getServiceResponse = async (domain, service, target, data) => {
    console.warn(`Calling service ${service} for ${domain}, target=${target}`);

    const response = await fetch(
      `/api/ha/service/${domain}/${service}?` +
        new URLSearchParams({
          target,
          data: JSON.stringify(data || {}),
        })
    );

    if (!response?.ok) {
      if ([400, 408].includes(response.status)) {
        const data = await response.json();
        throw new Error(data.detail);
      }
      throw new Error('Could not get service data');
    }

    const responseData = await response.json();
    return responseData[target];
  };

  const getCalendar = async (calendars) => {
    console.warn('Fetching calendar data');

    const query = new URLSearchParams(calendars.map((c) => ['calendar', c.entity]));
    const response = await fetch('/api/ha/calendar?' + query);

    if (!response?.ok) {
      if (response.status === 502) {
        throw new Error('Could not connect to Home Assistant');
      }
    }

    const data = await response.json();

    state.events = data;

    return state.events;
  };

  return {
    ...toRefs(state),
    getEntity,
    getEntities,
    getServiceResponse,
    getCalendar,
  };
}
