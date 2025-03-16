/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        apple: {
          blue: '#0071e3',
          darkblue: '#0077ED',
          gray: '#86868b',
          lightgray: '#f5f5f7',
          black: '#1d1d1f',
          white: '#ffffff',
        },
      },
      fontFamily: {
        sans: ['SF Pro Display', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
    },
  },
  daisyui: {
    themes: [
      {
        apple: {
          "primary": "#0071e3",
          "secondary": "#86868b",
          "accent": "#0077ED",
          "neutral": "#f5f5f7",
          "base-100": "#ffffff",
          "info": "#0071e3",
          "success": "#4BB543",
          "warning": "#FF9F0A",
          "error": "#FF3B30",
        },
      },
      "light",
    ],
  },
  plugins: [require("daisyui"), require("tailwind-scrollbar")],
  variants: {
    scrollbar: ["rounded"],
  },
};
