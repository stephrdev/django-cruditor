const babelParser = require('@babel/eslint-parser');
const js = require('@eslint/js');
const globals = require('globals');

module.exports = [
  js.configs.recommended,
  {
    ignores: [
      'coverage/**',
      'node_modules/**',
      'static/**',
      'build/**',
      'web/**',
      'htmlcov/**'
    ]
  },
  {
    languageOptions: {
      parser: babelParser,
      parserOptions: {
        requireConfigFile: false
      },
      ecmaVersion: 6,
      sourceType: 'module',
      globals: {
        ...globals.node,
        ...globals.browser
      }
    },
    rules: {
      'no-control-regex': 'off',
      'no-unused-vars': 'off'
    }
  }
];
