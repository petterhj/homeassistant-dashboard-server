/* eslint-disable no-undef */
/* eslint-disable prettier/prettier */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
    '../data/**/*.{yml,yaml}',
  ],
  // safelist: [
  //   { pattern: /(h|bg|border)-./ }
  // ],
  theme: {
    extend: {
      colors: {
        'white': '#ff00Ff',
      },
      fontFamily: {
        sans: ['Roboto'],
        // 'font-serif': ['Monda', 'cursive'],
      },
    },
  },
  plugins: [
    require('daisyui'),
    require('@tailwindcss/line-clamp'),
  ],
  daisyui: {
    themes: false,
    prefix: 'd-',
  },
};
