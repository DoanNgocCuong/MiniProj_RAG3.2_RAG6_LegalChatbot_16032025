import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 30001,
    host: true,
    strictPort: true,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://103.253.20.13:30000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    },
    hmr: {
      overlay: true
    },
    // Add server startup logging
    onBeforeMiddleware(server) {
      console.log('🚀 Starting development server...')
      console.log(`📁 Project root: ${server.config.root}`)
    },
    onAfterMiddleware(server) {
      console.log('🔌 Middleware setup complete')
    }
  },
  logLevel: 'info'
})
