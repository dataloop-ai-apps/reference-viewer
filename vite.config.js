import { defineConfig } from 'vite'
import Vue from '@vitejs/plugin-vue'
import eslintPlugin from 'vite-plugin-eslint'
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
    proxy: {
      '/api': {
        target: 'https://gate.dataloop.ai/api',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  plugins: [
    Vue(),
    eslintPlugin(),
    viteBasicSslPlugin(),
    Components({ resolvers: [IconsResolver()] }),
    Icons(),
  ],
})
