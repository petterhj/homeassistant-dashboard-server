<script setup>
import { computed } from 'vue';
import { useHomeAssistant } from '@/stores/homeassistant';
import { useCard } from '@/composables/card';
import { BASE_CARD_PROPS } from '@/util/card';
import BaseCard from '@/components/generic/BaseCard.vue';

const { getEntity } = useHomeAssistant();

const props = defineProps({
  ...BASE_CARD_PROPS,
  entity: {
    type: String,
    required: true,
  },
  title: {
    type: [String, Boolean],
    required: false,
    default: null,
  },
  icon: {
    type: String,
    required: false,
    default: 'lightning-bolt',
  },
});

const card = useCard(props);
const entity = await getEntity(props.entity);

const tileTitle = computed(() => {
  if (props.title === false) {
    return null;
  }

  if (props.title && props.title !== true) {
    return props.title;
  } else if (entity?.attributes?.friendly_name) {
    return entity.attributes.friendly_name;
  } else {
    return entity.id;
  }
});
</script>

<template>
  <BaseCard v-bind="card">
    <div class="flex items-center gap-4">
      <div>
        <div
          class="
            flex items-center justify-center
            bg-lightest rounded-full
            w-10 h-10
          "
        >
          <span class="mdi text-dark text-2xl" :class="`mdi-${icon}`" />
        </div>
      </div>

      <div class="flex flex-col flex-1">
        <div v-if="tileTitle" class="text-lg leading-5 font-semibold">
          {{ tileTitle }}
        </div>
        <div
          :class="[
            'flex',
            'justify-between',
            'font-medium',
            title === false ? 'text-md' : 'text-sm',
          ]"
        >
          <span class="text-light">
            {{ entity.state }}
          </span>
        </div>
      </div>
    </div>
  </BaseCard>
</template>
