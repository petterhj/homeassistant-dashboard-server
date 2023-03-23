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
    colors: {
      'dark': 'rgb(var(--color-dark) / <alpha-value>)',
      'light': 'rgb(var(--color-light) / <alpha-value>)',
      'lighter': 'rgb(var(--color-lighter) / <alpha-value>)',
      'lightest': 'rgb(var(--color-lightest) / <alpha-value>)',
    },
    extend: {
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
    styled: false,
    themes: false,
    base: false,
    prefix: 'd-',
  },
};
