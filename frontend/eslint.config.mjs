import globals from 'globals';
import js from '@eslint/js';
import stylisticJs from '@stylistic/eslint-plugin-js';
import pluginVue from 'eslint-plugin-vue';

export default [
  js.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  {
    plugins: {
      '@stylistic/js': stylisticJs,
    },
    languageOptions: {
      globals: {
        ...globals.node,
        ...globals.browser,
      },
    },
    files: ['**/*.js', '**/*.mjs', '**/*.vue'],
    rules: {
      '@stylistic/js/comma-dangle': ['error', {
        'arrays': 'always-multiline',
        'objects': 'always-multiline',
        'imports': 'always-multiline',
        'exports': 'always-multiline',
        'functions': 'never',
      }],
      '@stylistic/js/indent': ['error', 2, { 'SwitchCase': 1 }],
      '@stylistic/js/semi': ['error', 'always'],
      '@stylistic/js/quotes': ['error', 'single'],

      'vue/max-attributes-per-line': ['error', {
        'singleline': {
          'max': 5,
        },      
        'multiline': {
          'max': 1,
        },
      }],
      'vue/max-len': ['error', {
        'code': 90,
        'template': 90,
      }],
    },
  },
  {
    ignores: ['dist/', 'node_modules/'],
  },
];
