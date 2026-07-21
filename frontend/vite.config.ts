import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import VueRouter from 'vue-router/vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())

  return {
    plugins: [
      // Must run before vue(): scans src/pages and generates the typed routes
      // it transforms <route> blocks before the vue plugin compiles the SFC.
      VueRouter(),
      vue(),
      vueDevTools(),
      tailwindcss(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      proxy: {
        '/api': env.VITE_API_PROXY_TARGET,
      },
    },
  }
})
