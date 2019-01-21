module.exports = {
  "moduleNameMapper": {
        "\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$": "<rootDir>/tools/assetsTransformer.js",
        "\\.(css)$": "<rootDir>/tools/assetsTransformer.js"
      },
      "setupFiles": [
        "raf/polyfill",
        "./tools/setupJest.ts",

        "./tools/enzymeTestAdapterSetup.js"
  ],


  "roots": [
    "<rootDir>/src"
  ],
  "transform": {
    "^.+\\.(t|j)sx?$": "ts-jest"
  },
  "globals": {
    "_app_messages": {},
    "_app_conf": {}
  },

  "automock": false,


  "testRegex": "(/__tests__/.*|(\\.|/)(test|spec))\\.(t|j)sx?$",
  "moduleFileExtensions": [
    "ts",
    "tsx",
    "js",
    "jsx",
    "json",
    "node"
  ],
}
