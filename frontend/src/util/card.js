export const BASE_CARD_PROPS = {
  type: {
    type: String,
    required: true,
  },
  cardStyle: {
    type: [String, Object],
    required: false,
    default: null,
  },
  title: {
    type: [String, Boolean],
    required: false,
    default: null,
  },
  icon: {
    type: String,
    required: false,
    default: null,
  },
};

export const BASE_CARD_STYLE = [
  'flex',
  'flex-col',
  // 'h-full',
  'w-full',
  'overflow-hidden',
];
