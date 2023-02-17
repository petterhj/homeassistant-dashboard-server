<script setup>
import { useEntity } from '@/composables/entity.js';

import BaseCard from './BaseCard.vue';

const props = defineProps({
  entityId: {
    type: String,
    required: true,
  },
});

const entity = useEntity(props.entityId);

</script>

<template>
  <BaseCard :entity="entity">
    {{ entity }}
  </BaseCard>
</template>
