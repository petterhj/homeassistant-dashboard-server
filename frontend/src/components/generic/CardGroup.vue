<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useCard } from '@/composables/card';
import { BASE_CARD_PROPS } from '@/util/card';
import CardTitle from './CardTitle.vue';

const { query } = useRoute();

const props = defineProps({
  ...BASE_CARD_PROPS,
  type: {
    type: String,
    required: false,
    default: 'vertical-stack',
    validator(value) {
      return ['vertical-stack', 'horizontal-stack'].includes(value);
    },
  },
});
const card = useCard(props);

const flexGap = computed(() => {
  if (card.class) {
    const gap = card.class.split(' ').find((c) => c.startsWith('gap-'));
    if (gap) {
      return gap;
    }
  }
  return 'gap-4';
});
</script>

<template>
  <section
    v-bind="card"
    class="h-full"
    :style="[query?.debug === 'true' ? { border: '1px dashed red' } : null]"
  >
    <CardTitle v-if="title" :title="title" :icon="icon" />
    <div
      :class="[
        'flex',
        props.type === 'horizontal-stack' ? 'flex-row' : 'flex-col',
        'h-full',
        'w-full',
        flexGap,
      ]"
    >
      <slot />
    </div>
  </section>
</template>
