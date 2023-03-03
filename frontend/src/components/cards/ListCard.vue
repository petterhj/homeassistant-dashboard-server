<script setup>
import { computed } from 'vue';
import { useHomeAssistant } from '@/stores/homeassistant';

const { getEntityState } = useHomeAssistant();

const props = defineProps({
  entity: {
    type: String,
    required: true,
  },
  titleAttribute: {
    type: String,
    required: false,
    default: 'friendly_name',
  },
  itemsAttribute: {
    type: String,
    required: false,
    default: 'items',
  },
  titleProp: {
    type: String,
    required: false,
    default: 'title',
  },
  descriptionProp: {
    type: String,
    required: false,
    default: 'description',
  },
  icon: {
    type: String,
    required: false,
    default: null,
  },
  itemIcon: {
    type: String,
    required: false,
    default: null,
  },
});

const entity = await getEntityState(props.entity);

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
  <h1 v-if="title" class="mb-4 text-md text-gray-400 font-semibold uppercase">
    <span v-if="icon" class="mdi text-gray-400 mr-1" :class="['mdi-' + icon]" />
    {{ title }}
  </h1>

  <ul>
    <li
      v-for="(item, index) in items"
      :key="index"
      class="flex gap-2 ml-2 mb-1 items-center"
    >
      <span
        v-if="itemIcon || icon"
        :class="['mdi', `mdi-${itemIcon || icon}`, 'text-gray-400']"
      />
      <div class="flex flex-col">
        <span class="text-sm font-medium">{{ item.title }}</span>
        <p v-if="item.description" class="text-sm text-gray-600">
          {{ item.description }}
        </p>
      </div>
    </li>
  </ul>
</template>
