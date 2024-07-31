<script setup>
import { computed, ref, defineAsyncComponent, onErrorCaptured } from 'vue';
import { useI18n } from 'vue-i18n';
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

const card = ref(null);
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

  if (componentType.value === 'group') {
    return defineAsyncComponent(() => import('./generic/CardGroup.vue'));
  }

  console.group(`Loading component '${fileName}'`);
  for (const [key, value] of Object.entries(props.config)) {
    console.debug(`> ${key}:`, value);
  }
  console.groupEnd();

  return defineAsyncComponent(() => import(`./cards/${fileName}.vue`));
});

const cardProps = computed(() => {
  const { style, ...rest } = props.config;
  return {
    cardStyle: style,
    ...rest,
  };
});
</script>

<template>
  <template v-if="componentType === 'group'">
    <component
      :is="component"
      v-bind="cardProps"
      class="foo"
      bar="foo"
      sdasd="asdasd"
    >
      <ComponentLoader
        v-for="(componentConfig, index) in config.components"
        :key="index"
        :type="componentConfig.type"
        :config="componentConfig"
      />
    </component>
  </template>

  <template v-else>
    <Suspense v-if="!error">
      <template #default>
        <component
          :is="component"
          ref="card"
          v-bind="cardProps"
        />
      </template>

      <template #fallback>
        <LoadingState :message="config.type" />
      </template>
    </Suspense>

    <ErrorState
      v-else
      :title="t('general.noData')"
      :error="error"
    />
  </template>
</template>
