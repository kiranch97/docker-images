module.exports = {
  root: true,
  env: {
    browser: true
  },
  parserOptions: {
    parser: "babel-eslint"
  },
  extends: [
    "eslint:recommended",
    "plugin:vue/recommended",
  ],
  globals: {
    "process": "readonly",
  },
  rules: {
    "comma-dangle": [2, "always-multiline"],
    "no-console": "none",
    "no-debugger": process.env.NODE_ENV === "isProd" ? "error" : "warn",
    "prefer-const": "error",
    "quotes": [2, "double", {
        "allowTemplateLiterals": true
    }],
    "semi": [2, "always"],
    "space-before-function-paren": 1,
    "vue/attributes-order": [1, {
      "order": [
        "DEFINITION",
        "LIST_RENDERING",
        "CONDITIONALS",
        "RENDER_MODIFIERS",
        "GLOBAL",
        "UNIQUE",
        "TWO_WAY_BINDING",
        "OTHER_DIRECTIVES",
        "OTHER_ATTR",
        "EVENTS",
        "CONTENT"
      ]
    }],
    "vue/max-attributes-per-line": [2, {
      "singleline": 3,
      "multiline": {
         "max": 1,
         "allowFirstLine": false
       }
    }],
    "vue/require-component-is": 0,
    "vue/singleline-html-element-content-newline": 0,
  },
}
