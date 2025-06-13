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
        paul: {
          50: '#F9F7FC',
          100: '#F6EDFA',
          200: '#EBDBF3',
          300: '#DDBEE9',
          400: '#C997DB',
          500: '#B06EC7',
          600: '#8F4CA5',
          700: '#7B3E8D',
          800: '#1F2937',
          900: '#111827',
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
