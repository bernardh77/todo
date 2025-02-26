import { defineConfig } from 'vite'
import tailwindcss from 'tailwindcss'
import autoprefixer from 'autoprefixer'

export default defineConfig({
  css: {
    postcss: {
      plugins: [
        tailwindcss,
        autoprefixer,
      ],
    },
  },
  // If you're using Django, you might want to add these server settings
  server: {
    host: 'localhost',
    port: 5173,
    // Proxy API requests to Django development server
    proxy: {
      '/api': 'http://localhost:8000',
      '/admin': 'http://localhost:8000',
      '/static': 'http://localhost:8000',
    }
  }
})