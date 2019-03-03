module.exports = {
  "moduleNameMapper": {
    "\\.(jpg|jpeg|png|gif|eot|otf|webp|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$": "<rootDir>/tools/assetsTransformer.js",
    "\\.(css)$": "<rootDir>/tools/assetsTransformer.js",

    "^@Components/(.*)": "<rootDir>/src/js/components/$1",
    "^@Config/(.*)": "<rootDir>/src/js/config/$1",
    "^@Routes/(.*)": "<rootDir>/src/js/routes/$1",
    "^@Store/(.*)": "<rootDir>/src/js/store/$1",
    "^@Utils/(.*)": "<rootDir>/src/js/utils/$1",
    "^@Images/(.*)": "<rootDir>/src/images/$1"

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
    "^.+\\.(t|j)sx?$": "ts-jest",
    "^.+\\.svg$": "jest-svg-transformer"

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
