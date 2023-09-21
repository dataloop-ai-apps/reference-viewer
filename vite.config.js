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
    host: "0.0.0.0",
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
    viteBasicSslPlugin(),
    Components({ resolvers: [IconsResolver()] }),
    Icons(),
  ],
})
