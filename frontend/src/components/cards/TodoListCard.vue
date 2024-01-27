<script setup>
import MarkdownIt from 'markdown-it';
import { useI18n } from 'vue-i18n';
import { useHomeAssistant } from '@/stores/homeassistant';
import { useCard } from '@/composables/card';
import { BASE_CARD_PROPS } from '@/util/card';
import BaseCard from '@/components/generic/BaseCard.vue';

const { t } = useI18n();
const { getEntity, getServiceResponse } = useHomeAssistant();

const props = defineProps({
  ...BASE_CARD_PROPS,
  entity: {
    type: String,
    required: true,
  },
});

const card = useCard(props, {
  title: t('todo.todo'),
  icon: 'format-list-checks',
});

const entity = await getEntity(props.entity);
const friendlyName = entity?.attributes?.friendly_name;
if (!props.title && friendlyName) {
  card.title = friendlyName;
}

const markdown = new MarkdownIt();
const todos = await getServiceResponse('todo', 'get_items', props.entity);

function renderItem(itemSummary) {
  return markdown.render(itemSummary);
}
</script>

<template>
  <BaseCard v-bind="card">
    <ul>
      <li
        v-for="({ summary }, index) in todos?.items"
        :key="index"
        class="flex gap-2 mb-1 items-center"
      >
        <span class="mdi mdi-checkbox-blank-outline text-light" />
        <span class="text-sm font-medium" v-html="renderItem(summary)" />
      </li>
    </ul>
  </BaseCard>
</template>
