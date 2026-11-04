import { defineConfig } from 'vite'
import Vue from '@vitejs/plugin-vue'
import viteBasicSslPlugin from '@vitejs/plugin-basic-ssl'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import Components from 'unplugin-vue-components/vite'

// https://vitejs.dev/config/
export default defineConfig({
  base: '',
  server: {
    port: 3002,
    https: true,
    host: "local.dataloop.ai",
    proxy: {
      '/api': {
        target: 'https://gate.dataloop.ai/api',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  optimizeDeps: {
    include: ['lodash', 'pdfjs-dist', 'highlight.js'],
    exclude: ['node_modules', './node_modules', 'dist', './dist']
  },
  plugins: [
    Vue(),
    viteBasicSslPlugin(),
    Components({ resolvers: [IconsResolver()] }),
    Icons(),
  ],
  publicDir: "public",
  build: {
    // other build options
    rollupOptions: {
      outDir: "panels/reference-viewer",
      output: {
        manualChunks: {
          vendor: ['vue', 'pdfjs-dist'],
          // other chunk definitions
        },
      },
    },
  },
})

