import { fileURLToPath, URL } from 'node:url';
import { resolve } from 'path';
import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default ({ mode }) => {
  process.env = {
    ...process.env,
    ...loadEnv(mode, resolve(process.cwd(), '../')),
  };

  return defineConfig({
    envDir: '../',
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      proxy: {
        // https://vitejs.dev/config/server-options.html#server-proxy
        // https://github.com/http-party/node-http-proxy#options
        '/api': {
          // eslint-disable-next-line no-undef
          target: process.env.VITE_SERVER_URL,
          headers: { 'Content-Type': 'application/json' },
          // rewrite: (path) => path.replace(/\/api/, ''),
        },
      },
    },
  });
}
