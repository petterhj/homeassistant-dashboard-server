import { reactive } from 'vue';

export function useEntity(entity_id, config) {
  const entity = reactive({
    id: entity_id,
    state: null,
    attributes: null,
    last_changed: null,
    last_updated: null,
    history: [],
    error: null,
  });

  console.log(`Fetching state data for ${entity_id}`);

  fetch(
    `/ha/entity/${entity_id}?` +
      new URLSearchParams({
        history: config?.history || false,
      })
  )
    .then((res) => res.json())
    .then((json) => {
      if (json.detail) {
        console.error(json.detail);
        entity.error = json.detail;
        return;
      }

      entity.state = json.state;
      entity.attributes = json.attributes;
      entity.last_changed = json.last_changed;
      entity.last_updated = json.last_updated;
      entity.history = json.history;
    })
    .catch((err) => {
      console.error('Could not fetch state data', err);
      entity.error = err;
    });

  return entity;
}
