<script setup>
import { ref } from 'vue';
import { computed, defineAsyncComponent, onErrorCaptured } from 'vue';
import BaseCard from './cards/BaseCard.vue';

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
  error.value = err;
  return false;
});

const snakeToPascal = (str) => {
  let camelCase = str.replace(/([-_]\w)/g, (g) => g[1].toUpperCase());
  let pascalCase = camelCase[0].toUpperCase() + camelCase.substr(1);
  return pascalCase;
};

const componentType = computed(() => {
  return props?.config?.components ? 'group' : 'card';
});

const component = computed(() => {
  const fileName = `${snakeToPascal(`${props.type}-${componentType.value}`)}.vue`;
  const path = componentType.value === 'group' ? 'groups' : 'cards';
  console.group(`Loading component ${fileName}`);
  console.debug('> type', props.config.type);
  console.debug('> style', cardStyle.value);
  console.debug('> props', cardProps.value);
  console.groupEnd();
  return defineAsyncComponent(() => import(`./${path}/${fileName}`));
});

const cardStyle = computed(() => {
  const { style } = props.config;
  if (typeof style === 'object') {
    const b = Object.values(style).join(' ');
    console.warn(b);
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
    <component :is="component">
      <ComponentLoader
        v-for="(componentConfig, index) in config.components"
        :key="index"
        :type="componentConfig.type"
        :config="componentConfig"
      />
    </component>
  </template>
  <template v-else>
    <BaseCard :style="cardStyle" :error="error">
      <Suspense v-if="!error">
        <template #default>
          <component :is="component" v-bind="cardProps" />
        </template>
        <template #fallback>
          <div>Loading</div>
        </template>
      </Suspense>
    </BaseCard>
  </template>
</template>