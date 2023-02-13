<script setup>
import { computed } from 'vue';
import { useEntity } from '@/composables/entity.js';

import BaseCard from './BaseCard.vue';

const props = defineProps({
  entityId: {
    type: String,
    required: true,
  },
  titleAttribute: {
    type: String,
    required: false,
    default: null,
  },
  itemsAttribute: {
    type: String,
    required: true,
  },
  titleProp: {
    type: String,
    required: false,
    default: 'title',
  },
  descriptionProp: {
    type: String,
    required: false,
    default: null,
  },
  icon: {
    type: String,
    required: false,
    default: null,
  },
});

const entity = useEntity(props.entityId);

const title = computed(() => {
  if (
    !props.titleAttribute ||
    !entity.attributes ||
    !Object.prototype.hasOwnProperty.call(entity.attributes, props.titleAttribute)
  )
    return null;
  return entity.attributes[props.titleAttribute];
});

const items = computed(() => {
  if (
    !props.itemsAttribute ||
    !entity.attributes ||
    !Object.prototype.hasOwnProperty.call(entity.attributes, props.itemsAttribute)
  )
    return [];
  const items = entity.attributes[props.itemsAttribute]
  return items.map((item) => ({
    title: item[props.titleProp],
    description: item[props.descriptionProp],
  }));
});
</script>

<template>
  <BaseCard :entity="entity" :height="64">
    <h1 v-if="title" class="text-1xl font-semibold mb-2">
      {{ title }}
    </h1>
    <ul>
      <li v-for="(item, index) in items" :key="index" class="flex gap-2 ml-1 mb-2">
        <span v-if="icon" :class="['mdi', `mdi-${icon}`, 'text-gray-400']" />
        <div class="flex flex-col">
          <span class="text-md font-medium">{{ item.title }}</span>
          <p v-if="item.description" class="text-sm text-gray-600">
            {{ item.description }}
          </p>
        </div>
      </li>
    </ul>
  </BaseCard>
</template>
