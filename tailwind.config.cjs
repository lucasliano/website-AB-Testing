module.exports = {
  content: [
    "./app/templates/**/*.{html,js}",
    "./app/static/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          bg: "#F5F5F7",
          primary: "#004C8C",
          secondary: "#1D9A6C"
        }
      }
    }
  },
  plugins: []
};
