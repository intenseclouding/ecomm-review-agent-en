/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      width: {
        '70': '280px',
        '64': '256px',
        '60': '240px',
      },
      margin: {
        '280': '280px',
        '256': '256px',
        '240': '240px',
      },
    },
  },
  plugins: [],
}