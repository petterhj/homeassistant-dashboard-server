<script setup>
import { computed } from 'vue';
import { useHomeAssistant } from '@/stores/homeassistant';
import CardTitle from './partials/CardTitle.vue';

const { getEntity } = useHomeAssistant();

const props = defineProps({
  entity: {
    type: String,
    required: true,
  },
  itemCount: {
    type: Number,
    required: false,
    default: 10,
  },
  title: {
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

const entity = await getEntity(props.entity);

const items = computed(() => {
  if (!entity || !entity.attributes?.torrent_info) {
    return [];
  }
  return entity.attributes.torrent_info;
});

const getIcon = (item) => {
  switch (item.status) {
    case 'seeding':
      return 'arrow-up-thick';
    case 'downloading':
      return 'arrow-down-thick';
    case 'stopped':
      return 'pause';
    default:
      return '';
  }
};
</script>

<template>
  <CardTitle :title="title" :icon="icon" />

  <ul>
    <li
      v-for="(item, name, index) in items"
      :key="index"
      class="flex gap-2 ml-2 items-center"
    >
      <span
        :class="[
          'mdi',
          `mdi-${getIcon(item)}`,
          item.status === 'stopped' ? 'text-gray-300' : 'text-gray-400',
        ]"
      />
      <div class="flex flex-col">
        <span
          class="text-sm line-clamp-1 text-ellipsis"
          :class="{ 'text-gray-300': item.status === 'stopped' }"
          >{{ name }}</span
        >
      </div>
    </li>
  </ul>
</template>
