import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Build to Django's static directory
    outDir: '../static',
    assetsDir: '',
    manifest: true,
    rollupOptions: {
      input: './src/main.jsx',
      output: {
        entryFileNames: 'main.js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name][extname]',
      },
    },
  },
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    }
  }
})
