import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [svelte()],
  resolve: {
    alias: {
      $lib: '/src/lib'
    }
  },
  server: {
    host: true, // Needed for Docker
    port: 5173,
    watch: {
      usePolling: true // Often needed for Windows/WSL file watching
    }
  }
})
