/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx}'
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Literata"', 'serif'],
        body: ['"Be Vietnam Pro"', 'system-ui', 'sans-serif']
      },
      colors: {
        ink: {
          900: '#0b0b14',
          800: '#151528',
          700: '#1d1f38'
        },
        gold: {
          500: '#e6b35a',
          400: '#f2c77b'
        },
        nebula: {
          500: '#6b7cff',
          400: '#8f9bff'
        },
        pink: {
          500: '#f4a6c1',
          400: '#f7b9cf',
          300: '#f9cfe0'
        },
        mint: {
          500: '#9fe3c8',
          400: '#b8ecd6'
        }
      },
      backgroundImage: {
        'hero-glow': 'radial-gradient(circle at top, rgba(107,124,255,0.35), transparent 60%)',
        'paper-texture': 'linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0))'
      },
      boxShadow: {
        soft: '0 20px 60px rgba(11, 11, 20, 0.4)'
      }
    }
  },
  plugins: []
}
