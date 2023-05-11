<script setup>
import { computed, ref, defineAsyncComponent, onErrorCaptured } from 'vue';
import { useI18n } from 'vue-i18n';
import BaseCard from './cards/BaseCard.vue';
import LoadingState from './LoadingState.vue';
import ErrorState from './ErrorState.vue';

const { t } = useI18n();

const props = defineProps({
  type: {
    type: String,
    required: true,
  },
  config: {
    type: Object,
    required: true,
  },
});

const error = ref(null);

onErrorCaptured((err) => {
  console.error('Error while loading component:', err.message);
  console.debug(err);
  if (err?.message.startsWith('Unknown variable dynamic import')) {
    error.value = new Error(`Unknown card type ${props.type}`);
  } else {
    error.value = err;
  }
  return false;
});

const snakeToPascal = (str) => {
  let camelCase = str.replace(/([-_]\w)/g, (g) => g[1].toUpperCase());
  let pascalCase = camelCase[0].toUpperCase() + camelCase.substr(1);
  return pascalCase;
};

const componentType = computed(() => {
  if (Object.prototype.hasOwnProperty.call(props?.config, 'components')) {
    return 'group';
  } else {
    return 'card';
  }
});

const component = computed(() => {
  const fileName = `${snakeToPascal(`${props.type}-${componentType.value}`)}`;
  const path = componentType.value === 'group' ? 'groups' : 'cards';
  console.group(`Loading component ${fileName}`);
  console.debug('> type:', props.config.type);
  console.debug('> style:', cardStyle.value);
  console.debug('> props:', cardProps.value);
  console.groupEnd();
  return defineAsyncComponent(() => import(`./${path}/${fileName}.vue`));
});

const cardStyle = computed(() => {
  const { style } = props.config;
  if (typeof style === 'object') {
    const b = Object.values(style).join(' ');
    return b;
  } else if (typeof style === 'string') {
    return style;
  }
  return '';
});

const cardProps = computed(() => {
  // eslint-disable-next-line no-unused-vars
  const { type, style, ...rest } = props.config;
  return rest;
});
</script>

<template>
  <template v-if="componentType === 'group'">
    <component :card-style="cardStyle" :is="component">
      <ComponentLoader
        v-for="(componentConfig, index) in config.components"
        :key="index"
        :type="componentConfig.type"
        :config="componentConfig"
      />
    </component>
  </template>

  <template v-else>
    <BaseCard :type="config.type" :card-style="cardStyle">
      <Suspense v-if="!error">
        <template #default>
          <component :is="component" v-bind="cardProps" />
        </template>

        <template #fallback>
          <LoadingState :message="config.type" />
        </template>
      </Suspense>

      <ErrorState v-else :title="t('general.noData')" :error="error" />
    </BaseCard>
  </template>
</template>
