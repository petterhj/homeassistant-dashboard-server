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
  iconItem: {
    type: String,
    required: false,
    default: null,
  }
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
  const items = entity.attributes[props.itemsAttribute];
  return items.map((item) => ({
    title: item[props.titleProp],
    description: item[props.descriptionProp],
  }));
});
</script>

<template>
  <BaseCard :entity="entity" :title="title" :icon="icon">
    <ul>
      <li v-for="(item, index) in items" :key="index" class="flex gap-2 ml-2 mb-1">
        <span
          v-if="iconItem || icon"
          :class="['mdi', `mdi-${iconItem || icon}`, 'text-gray-400']"
        />
        <div class="flex flex-col">
          <span class="text-sm font-medium">{{ item.title }}</span>
          <p v-if="item.description" class="text-sm text-gray-600">
            {{ item.description }}
          </p>
        </div>
      </li>
    </ul>
  </BaseCard>
</template>
