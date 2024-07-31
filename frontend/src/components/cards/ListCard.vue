<script setup>
import { computed } from 'vue';
import { useHomeAssistant } from '@/stores/homeassistant';
import { BASE_CARD_PROPS } from '@/util/card';
import BaseCard from '@/components/generic/BaseCard.vue';

const { getEntity } = useHomeAssistant();

const props = defineProps({
  ...BASE_CARD_PROPS,
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
  itemIcon: {
    type: String,
    required: false,
    default: null,
  },
});

const entity = await getEntity(props.entity);

// const title = computed(() => {
//   if (
//     !props.titleAttribute ||
//     !entity.attributes ||
//     !Object.prototype.hasOwnProperty.call(entity.attributes, props.titleAttribute)
//   )
//     return null;
//   return entity.attributes[props.titleAttribute];
// });

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
  <BaseCard v-bind="card">
    <ul>
      <li
        v-for="(item, index) in items"
        :key="index"
        class="flex gap-2 mb-1 items-center"
      >
        <span
          v-if="itemIcon || icon"
          :class="['mdi', `mdi-${itemIcon || icon}`, 'text-light']"
        />
        <div class="flex flex-col">
          <span class="text-sm font-medium">{{ item.title }}</span>
          <p v-if="item.description" class="text-xs text-light font-medium">
            {{ item.description }}
          </p>
        </div>
      </li>
    </ul>
  </BaseCard>
</template>
