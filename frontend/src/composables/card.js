import { computed, reactive, ref } from 'vue';
import { twMerge } from 'tailwind-merge';
import { BASE_CARD_STYLE } from '@/util/card';

export function useCard(props, options) {
  const title = ref(
    props.title === false
      ? null
      : typeof props.title === 'string'
        ? props.title
        : options?.title || null
  );
  const icon = ref(
    props.icon === false
      ? null
      : typeof props.icon === 'string'
        ? props.icon
        : options?.icon || null
  );
  const style = ref(options?.style || []);

  console.group('Card:');
  console.log('> props:', props);
  console.log('> type:', props.type);
  console.log('> style:', props.cardStyle);
  console.log('> title:', title.value);
  console.log('> icon:', icon.value);
  console.groupEnd();

  const cardStyle = computed(() => {
    let propStyles = [];
    if (props.cardStyle) {
      if (typeof props.cardStyle === 'object') {
        propStyles = Object.values(props.cardStyle);
      } else if (typeof props.cardStyle === 'string') {
        propStyles = props.cardStyle.split(' ');
      }
    }
    return twMerge(BASE_CARD_STYLE, style.value, propStyles);
  });

  return reactive({
    type: props.type,
    class: cardStyle,
    title,
    icon,
  });
}
