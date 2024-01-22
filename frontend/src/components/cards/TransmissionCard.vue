<script setup>
// Transmission
// https://www.home-assistant.io/integrations/transmission/
// The Transmission integration allows you to monitor your Transmission
// BitTorrent downloads from within Home Assistant and set up automations
// based on that information.
import { computed } from 'vue';
import { parseISO } from 'date-fns';
import { useHomeAssistant } from '@/stores/homeassistant';
import { useCard } from '@/composables/card';
import { BASE_CARD_PROPS } from '@/util/card';
import BaseCard from '@/components/generic/BaseCard.vue';

const { getEntity } = useHomeAssistant();

const props = defineProps({
  ...BASE_CARD_PROPS,
  entity: {
    type: String,
    required: false,
    default: 'sensor.transmission_total_torrents',
  },
  limit: {
    type: Number,
    required: false,
    default: 15,
  },
});

const entity = await getEntity(props.entity);
const card = useCard(props, {
  title: 'Transmission',
  icon: 'download',
});

const items = computed(() => {
  if (!entity || !entity.attributes?.torrent_info) {
    return [];
  }
  return Object.keys(entity.attributes.torrent_info)
    .map((name) => {
      return { name, ...entity.attributes.torrent_info[name] };
    })
    .slice(0, props.limit)
    .sort((a, b) => parseISO(b.added_date) - parseISO(a.added_date));
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
  <BaseCard v-bind="card">
    <ul class="w-full">
      <li
        v-for="(item, name, index) in items"
        :key="index"
        class="flex gap-2 ml-2 items-center"
      >
        <span
          :class="[
            'mdi',
            `mdi-${getIcon(item)}`,
            item.status === 'stopped' ? 'text-lighter' : 'text-light',
          ]"
        />
        <span
          class="text-sm font-medium line-clamp-1 text-ellipsis"
          :class="{ 'text-lighter': item.status === 'stopped' }"
        >
          {{ item.name }}
        </span>
      </li>
    </ul>
  </BaseCard>
</template>
