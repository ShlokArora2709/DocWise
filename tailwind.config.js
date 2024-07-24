/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.{html,js}',  // Adjust paths based on your project structure
    './static/**/*.{html,js}',
    './Login/static/**/*.{html,js}', 

  ],
  theme: {
    extend: {
      colors: {
        'custom-fuchsia': '#4a053b',
        'custom-blue': '#312e81',
        'custom-yellow': '#e9df0e',
        'custom-teal': '#31e4b3',
        'custom-pink': '#e72da2',
        'custom-orange': '#e69500' // dim shade of orange
      }
    }
  },
  variants: {},
  plugins: [],
}
