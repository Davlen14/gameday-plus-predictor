import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    strictPort: true,
    host: '0.0.0.0',
    cors: true,
    open: false,
    hmr: {
      overlay: true
    }
  },
  // CRITICAL FIX: Pre-bundle all heavy dependencies
  optimizeDeps: {
    include: [
      // Radix UI packages (30+ packages = hundreds of modules)
      '@radix-ui/react-dialog',
      '@radix-ui/react-dropdown-menu',
      '@radix-ui/react-select',
      '@radix-ui/react-tabs',
      '@radix-ui/react-popover',
      '@radix-ui/react-tooltip',
      '@radix-ui/react-accordion',
      '@radix-ui/react-alert-dialog',
      '@radix-ui/react-avatar',
      '@radix-ui/react-checkbox',
      '@radix-ui/react-collapsible',
      '@radix-ui/react-context-menu',
      '@radix-ui/react-hover-card',
      '@radix-ui/react-label',
      '@radix-ui/react-menubar',
      '@radix-ui/react-navigation-menu',
      '@radix-ui/react-progress',
      '@radix-ui/react-radio-group',
      '@radix-ui/react-scroll-area',
      '@radix-ui/react-separator',
      '@radix-ui/react-slider',
      '@radix-ui/react-switch',
      '@radix-ui/react-toast',
      '@radix-ui/react-toggle',
      '@radix-ui/react-toggle-group',
      '@radix-ui/react-aspect-ratio',
      // Other heavy UI libraries
      'lucide-react',
      'recharts',
      'zustand'
    ],
    force: true // Force immediate optimization
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-radix': ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu', '@radix-ui/react-select'],
          'vendor-ui': ['lucide-react', 'recharts'],
          'react-vendor': ['react', 'react-dom']
        }
      }
    }
  }
})
