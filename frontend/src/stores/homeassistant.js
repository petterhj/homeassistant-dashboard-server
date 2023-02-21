import { reactive, toRefs, onMounted } from 'vue';

const state = reactive({
  config: {},
  entities: {},
});

console.log('Fetching Home Assistant config...')
const response = await fetch(`/proxy/ha/config`);
const data = await response.json();
state.config = data;

export function useHomeAssistant() {
  const getEntityState = async (entityId, options) => {
    if (Object.prototype.hasOwnProperty.call(state.entities, entityId)) {
      console.debug(`Returning cached entity state for ${entityId}`);
      return state.entities[entityId];
    }

    const fetchHistory = !!options?.history;

    console.warn(`Fetching entity state for ${entityId}, history=${fetchHistory}`);
    const response = await fetch(
      `/proxy/ha/entity/${entityId}?` + new URLSearchParams({ history: fetchHistory })
    );
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

  return { ...toRefs(state), getEntityState };
}
