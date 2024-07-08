module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true, // This adds Node.js global variables and Node.js scoping
  },
  extends: [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:@typescript-eslint/recommended",
  ],
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["react", "@typescript-eslint"],
  rules: {
    "no-undef": "off", // This turns off the rule for undefined variables
  },
};
