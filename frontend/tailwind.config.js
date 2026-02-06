/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}'
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
        'paper-texture': 'linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0))',
        'glass-gradient': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05))'
      },
      boxShadow: {
        soft: '0 20px 60px rgba(11, 11, 20, 0.4)',
        glow: '0 0 15px rgba(230, 179, 90, 0.3)',
        'glow-nebula': '0 0 15px rgba(107, 124, 255, 0.3)'
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'slide-up': 'slideUp 0.6s ease-out forwards',
        'float': 'float 6s ease-in-out infinite'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' }
        }
      }
    }
  },
  plugins: []
}
