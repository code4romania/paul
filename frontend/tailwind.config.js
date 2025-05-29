/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#FFF0A6',
          main: '#FEE600',
          dark: '#FFD403',
        },
        secondary: {
          main: '#E3F1EA',
        },
        yellow: {
          600: '#F9BB30',
          500: '#FEE600',
          400: '#FFF0A6',
        },
        gray: {
          400: '#F1EDE6',
          500: '#7E827F',
        },
        black: '#2B2D33',
        'warm-grey': '#F1EDE6',
        'off-black': '#2B2D33',
        'green-highlight': '#A3E2CC',
        'green-mid-tone': '#67D0AB',
        'purple-highlight': '#9D88D9',
        'purple-mid-tone': '#6A4CAD',
        error: '#C65C4A',
      },
      fontFamily: {
        sans: ['Amalia-Regular', 'sans-serif'],
        'amalia-medium': ['Amalia-Medium', 'sans-serif'],
        'amalia-bold': ['Amalia-Bold', 'sans-serif'],
      },
      fontSize: {
        '2xs': '0.625rem',
        xs: '0.75rem',
      },
    },
  },
  plugins: [],
};
