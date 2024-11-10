import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Makes it accessible over the network
    port: 3000, // Set your preferred port (default is usually 5173 for Vite)
  },
})
