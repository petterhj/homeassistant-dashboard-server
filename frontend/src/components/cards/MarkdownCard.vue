<script setup>
import MarkdownIt from 'markdown-it';
import { computed, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useCard } from '@/composables/card';
import { useHomeAssistant } from '@/stores/homeassistant';
import { BASE_CARD_PROPS } from '@/util/card';
import BaseCard from '@/components/generic/BaseCard.vue';

const { t } = useI18n();

const props = defineProps({
  ...BASE_CARD_PROPS,
  entity: {
    type: String,
    required: false,
    default: null,
  },
  attribute: {
    type: String,
    required: false,
    default: null,
  },
  content: {
    type: String,
    required: false,
    default: null,
  },
});
const card = useCard(props, {
  title: 'Markdown',
  icon: 'text',
});

const entityState = ref(null);

if (!props.content && props.entity) {
  const { getEntity } = useHomeAssistant();
  entityState.value = await getEntity(props.entity);
  const friendlyName = entityState.value?.attributes?.friendly_name;
  if (!props.title && friendlyName) {
    card.title = friendlyName;
  }
}

const content = computed(() => {
  const markdown = new MarkdownIt();
  if (props.content) {
    return markdown.render(props.content);
  } else if (entityState.value) {
    const content =
      entityState.value.attributes[props.attribute] || entityState.value.state;
    return markdown.render(content);
  } else {
    return t('general.noData');
  }
});
</script>

<template>
  <BaseCard v-bind="card">
    <div class="text-sm" v-html="content" />
  </BaseCard>
</template>

<style scoped>
:deep(h1),
:deep(h2),
:deep(h3) {
  @apply font-medium mb-0.5;
}
:deep(p) {
  @apply mb-1;
}
</style>
