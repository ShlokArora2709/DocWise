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
        'custom-fuchsia': '#120021',
        'custom-blue': '#00001c',
        'custom-yellow': '#e9df0e',
        'custom-teal': '#31e4b3',
        'custom-pink': '#e72da2',
        'custom-orange': '#e69500',
        'custom-blue-2':'#130057',
        'custom-gray-blue':'#302a3d'
      },
      spacing: {
        '128': '32rem', // Adjust as needed
        '144': '36rem', // Add more custom values if needed
      }
    }
  },
  variants: {},
  plugins: [],
}
