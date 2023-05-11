<script setup>
import { useHomeAssistant } from '@/stores/homeassistant';

const { getEntity } = useHomeAssistant();

const props = defineProps({
  entity: {
    type: String,
    required: true,
  },
});

const entity = await getEntity(props.entity);
</script>

<template>
  <BaseCard :entity="entity">
    {{ entity }}
  </BaseCard>
</template>
