<script setup>
import { ref, computed, onMounted } from 'vue';
import { format } from 'date-fns';
import { useCard } from '@/composables/card';
import { BASE_CARD_PROPS } from '@/util/card';
import BaseCard from '@/components/generic/BaseCard.vue';

const items = ref([]);

const props = defineProps({
  ...BASE_CARD_PROPS,
  url: {
    type: String,
    required: true,
  },
  limit: {
    type: Number,
    required: false,
    default: 10,
  },
  showCategories: {
    type: Boolean,
    required: false,
    default: true,
  },
  showDescription: {
    type: Boolean,
    required: false,
    default: true,
  },
  dateFormat: {
    type: String,
    required: false,
    default: 'HH:mm',
  },
  lineClamp: {
    type: Number,
    required: false,
    default: 3,
  },
});

const card = useCard(props, {
  title: 'RSS',
  icon: 'rss-box',
});

const lineClampClass = computed(() => {
  return props.lineClamp > 0 ? `line-clamp-${props.lineClamp}` : null;
});

onMounted(() => {
  console.debug(`Fetching RSS data from ${props.url}`);

  fetch(props.url)
    .then((response) => response.text())
    .then((str) => new window.DOMParser().parseFromString(str, 'text/xml'))
    .then((data) => {
      if (!props.title) {
        try {
          const feedTitle = data
            .querySelector('channel')
            .querySelector('title').innerHTML;
          card.title = feedTitle;
        } catch {
          /* pass */
        }
      }

      items.value = [...data.querySelectorAll('item')].map((item) => ({
        title: item.querySelector('title').innerHTML,
        description: item.querySelector('description').innerHTML,
        categories: [...item.querySelectorAll('category')].map(
          (category) => category.innerHTML
        ),
        datetime: new Date(item.querySelector('pubDate').innerHTML),
      }));
    });
});
</script>

<template>
  <BaseCard v-bind="card">
    <div v-if="items.length" class="flex flex-col px-2">
      <div
        v-for="(item, index) in items.slice(0, limit)"
        :key="index"
        class="rss-item relative text-sm pl-4"
      >
        <div
          v-if="showCategories && item.categories.length"
          class="flex gap-3 pt-[2px] mb-1 line-clamp-1"
        >
          <span
            v-for="category in item.categories"
            :key="category"
            class="rss-item__category relative text-xs font-medium text-lighter whitespace-nowrap"
          >
            {{ category }}
          </span>
        </div>

        <div class="rss-item__inner mb-3 max-h-32">
          <span v-if="item.datetime" class="mr-2 font-medium text-lighter">
            {{ format(item.datetime, props.dateFormat) }}
          </span>
          <span class="mr-2 font-medium">
            {{ item.title }}
          </span>
          <span
            v-if="showDescription && item.description"
            :class="['text-light', 'text-xs', lineClampClass]"
          >
            {{ item.description }}
          </span>
        </div>
      </div>
    </div>
  </BaseCard>
</template>

<style scoped>
.rss-item {
  border-left: 2px solid var(--color-lightest-rgb);
}

.rss-item:before {
  position: absolute;
  top: 3px;
  left: -7px;
  width: 12px;
  height: 12px;
  border: 4px solid var(--color-lighter-rgb);
  background: #ffffff;
  outline: 6px solid #ffffff;
  border-radius: 50%;
  content: '';
}

.rss-item__category:not(:last-of-type):after {
  position: absolute;
  content: '/';
  right: -0.5rem;
}
</style>
