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

  fetch(`/api/states/${entity_id}`)
    .then((res) => res.json())
    .then((json) => {
      if (json.message) {
        entity.error = json.message;
        return;
      }
      entity.state = json.state;
      entity.attributes = json.attributes;
      entity.last_changed = json.last_changed;
      entity.last_updated = json.last_updated;

      if (config?.history) {
        console.log(`Fetching state history for ${entity_id}`);

        fetch(`/api/history/period?filter_entity_id=${entity_id}`)
          .then((res) => res.json())
          .then((json) => {
            entity.history = json.length ? json[0] : [];
          })
          .catch((err) => {
            console.error('Could not fetch history data', err);
            entity.error = err;
          });
      }
    })
    .catch((err) => {
      console.error('Could not fetch state data', err);
      entity.error = err;
    });

  return entity;
}
