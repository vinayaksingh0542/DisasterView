/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0B0F19',
        surface: '#151A23',
        primary: '#3B82F6',
        warning: '#F59E0B',
        critical: '#EF4444',
        safe: '#10B981',
      }
    },
  },
  plugins: [],
}
