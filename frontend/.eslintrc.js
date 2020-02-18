module.exports = {
  'env': {
    'browser': true,
    'es6': true,
  },
  'parser': '@typescript-eslint/parser',
  'parserOptions': {
    'project': 'tsconfig.json',
    'sourceType': 'module'
  },
  'extends': [
    'airbnb',
    'airbnb/hooks',
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:@typescript-eslint/recommended'
  ],
  'plugins': [
    'prettier',
    'react',
    'react-hooks',
    'import'
  ],
  'rules': {
    'indent': [ 'error', 2 ],
    'max-len': [ 'error', {
      'code': 120,
    } ],
    'array-bracket-spacing': [ 'error', 'always' ],
    'computed-property-spacing': [ 'error', 'always' ],
    'import/order': [ 'error', {
      'newlines-between': 'always',
      'alphabetize': {
        'order': 'asc',
        'caseInsensitive': true,
      },
      'groups': [
        'builtin',
        'external',
        'internal',
        'parent',
        'sibling',
        'index.tsx',
      ],
      'pathGroupsExcludedImportTypes': [ 'builtin' ],
      'pathGroups': [ {
        'pattern': '@Store/**',
        'group': 'internal',
      }, {
        'pattern': '@Config/**',
        'group': 'internal',
      }, {
        'pattern': '@Utils/**',
        'group': 'internal',
      }, {
        'pattern': '@Components/**',
        'group': 'internal',
      }, {
        'pattern': '@Navigation/**',
        'group': 'internal',
      }, {
        'pattern': '@Styles/**',
        'group': 'internal',
      }, {
        'pattern': '@Images/**',
        'group': 'internal',
      }, {
        'pattern': '@Mocks/**',
        'group': 'internal',
      }, {
        'pattern': '@Graphql/**',
        'group': 'internal',
      } ],
    } ],
    'max-lines': [ 'error', {
      max: 600,
    } ],
    'no-trailing-spaces': [
      'error',
    ],
    'camelcase': [ 'off' ],
    'import/no-unresolved': [ 'off' ],
    'import/extensions': [ 'off' ],
    '@typescript-eslint/camelcase': [ 'off' ],
    'object-curly-newline': [ 'error', {
      'ImportDeclaration': 'never',
    } ],
    // Could turn this on, as gives useful/annoying warnings.
    '@typescript-eslint/no-explicit-any': [ 'off' ],
    // Same as no-explicit-any
    '@typescript-eslint/explicit-function-return-type': [ 'off' ],
    'react/jsx-filename-extension': [ 'error', {
      'extensions': [ '.jsx', '.tsx' ],
    } ],
    'react/jsx-props-no-spreading': [ 'off' ],
    'react/destructuring-assignment': [ 'off' ],
    'padded-blocks': [ 'off' ],
    '@typescript-eslint/no-empty-interface': [ 'off' ],
    'arrow-body-style': [ 'off' ],
    'implicit-arrow-linebreak': [ 'off' ],
    'no-confusing-arrow': [ 'off' ],
    'operator-linebreak': [ 'off' ],
    '@typescript-eslint/no-use-before-define': [ 'off' ],
    'import/prefer-default-export': [ 'off' ],
    '@typescript-eslint/no-empty-function': [ 'off' ],
    'import/no-extraneous-dependencies': [ 'error', {
      'devDependencies': [ '**/*.spec.tsx', '**/*.spec.ts', '**/*.stories.tsx', '**/*.stories.ts' ],
    } ],
    'arrow-parens': [ 'off' ],
    'react/prop-types': [ 'off' ],
    'jsx-a11y/label-has-associated-control': [ 'off' ],
    'react/jsx-boolean-value': [ 'off' ],
    'no-underscore-dangle': [ 'off' ],
    'react/button-has-type': [ 'off' ],
  }
};
