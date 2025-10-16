/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // Enable class-based dark mode
  theme: {
    extend: {
      /* ============================================
         🎨 CUSTOM COLOR SYSTEM  
         ============================================ */
      colors: {
        /* Enhanced slate palette */
        'slate': {
          900: '#0f172a', 800: '#1e293b', 700: '#334155',
          600: '#475569', 500: '#64748b', 400: '#94a3b8',
          300: '#cbd5e1', 200: '#e2e8f0', 100: '#f1f5f9'
        },

        /* Design system colors from globals.css */
        background: 'var(--background)',
        foreground: 'var(--foreground)',
        card: 'var(--card)',
        'card-foreground': 'var(--card-foreground)',
        popover: 'var(--popover)',
        'popover-foreground': 'var(--popover-foreground)',
        primary: 'var(--primary)',
        'primary-foreground': 'var(--primary-foreground)',
        secondary: 'var(--secondary)',
        'secondary-foreground': 'var(--secondary-foreground)',
        muted: 'var(--muted)',
        'muted-foreground': 'var(--muted-foreground)',
        accent: 'var(--accent)',
        'accent-foreground': 'var(--accent-foreground)',
        destructive: 'var(--destructive)',
        'destructive-foreground': 'var(--destructive-foreground)',
        border: 'var(--border)',
        input: 'var(--input)',
        ring: 'var(--ring)',

        /* Sport-specific colors */
        team: {
          home: '#ff5f05',
          away: '#ce1141',
        },

        /* Analytical colors */
        metric: {
          positive: '#10b981',
          negative: '#ef4444',
          neutral: '#06b6d4',
          warning: '#f59e0b',
        }
      },

      /* ============================================
         📏 SPACING & SIZING
         ============================================ */
      borderRadius: {
        'xs': '0.125rem',
        'sm': '0.25rem',
        'md': '0.375rem',
        'lg': '0.5rem',
        'xl': '0.75rem',
        '2xl': '1rem',
      },

      /* ============================================
         🔤 TYPOGRAPHY SYSTEM
         ============================================ */
      fontFamily: {
        'sans': ['Orbitron', 'sans-serif'],
        'orbitron': ['Orbitron', 'sans-serif'],
        'mono': ['SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Courier New', 'monospace'],
      },

      /* ============================================
         🎬 ANIMATION SYSTEM
         ============================================ */
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-in-left': 'slideInLeft 0.4s ease-out',
        'slide-in-right': 'slideInRight 0.4s ease-out',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',
      },

      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInLeft: {
          '0%': { opacity: '0', transform: 'translateX(-30px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(30px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        pulseGlow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(16, 185, 129, 0.2)' },
          '50%': { boxShadow: '0 0 30px rgba(16, 185, 129, 0.4)' },
        },
      },

      /* ============================================
         🎨 BACKDROP & EFFECTS
         ============================================ */
      backdropBlur: {
        'xs': '2px',
        'sm': '4px',
        'md': '12px',
        'lg': '16px',
        'xl': '24px',
        '2xl': '40px',
        '3xl': '64px',
      },

      /* ============================================
         📱 RESPONSIVE BREAKPOINTS
         ============================================ */
      screens: {
        'xs': '475px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      },
    },
  },
  plugins: [],
}