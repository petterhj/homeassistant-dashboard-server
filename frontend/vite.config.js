import { fileURLToPath, URL } from 'node:url';

import { defineConfig, loadEnv } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default ({ mode }) => {
  // eslint-disable-next-line no-undef
  process.env = { ...process.env, ...loadEnv(mode, process.cwd()) };

  return defineConfig({
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      proxy: {
        // https://vitejs.dev/config/server-options.html#server-proxy
        // https://github.com/http-party/node-http-proxy#options
        '/api': {
          // eslint-disable-next-line no-undef
          target: process.env.VITE_HOMEASSISTANT_URL,
          // Changes the origin of the host header to the target URL
          changeOrigin: true,
          secure: false,
          // Extra headers to be added to target requests
          headers: {
            // eslint-disable-next-line prettier/prettier, no-undef
            'Authorization': `Bearer ${process.env.VITE_HOMEASSISTANT_TOKEN}`,
            'Content-Type': 'application/json',
            'User-Agent': 'HomeAssistantInkplateDashboard/0.1.0',
          },
          configure: (proxy, options) => {
            // Emitted before the data is sent, allowing one to alter the
            // proxyReq request object.
            proxy.on('proxyReq', (proxyReq, req, res) => {
              console.info(`Proxy request: ${req.method} ${req.url}`);
              // console.log(res);
            });
            // Emitted if the request to the target got a response.
            proxy.on('proxyRes', (proxyRes, req, res) => {
              console.info(`Proxy response: ${proxyRes.statusCode} ${req.url}`);
            });
            // Emitted if the request to the target fail.
            proxy.on('error', (err, req, res) => {
              // res.writeHead(500, { 'Content-Type': 'text/plain' });
              // res.end(
              //   'Something went wrong. And we are reporting a custom error message.'
              // );
              // console.log('------------------');
              // console.log(res);
              // console.log('------------------');
              // console.log(res);
              // console.log('------------------');
            });
          },
        },
      },
    },
  });
}
