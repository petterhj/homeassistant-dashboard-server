module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
    '../data/**/*.{yml,yaml}',
  ],
  safelist: [
    { pattern: /grid-cols-.+/ },
    { pattern: /(h|bg|border|gap|basis|line-clamp|)-./ },
  ],
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
      },
    },
  },
};
