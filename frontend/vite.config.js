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
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      proxy: {
        // https://vitejs.dev/config/server-options.html#server-proxy
        // https://github.com/http-party/node-http-proxy#options
        '/ha': {
          // eslint-disable-next-line no-undef
          target: process.env.VITE_PROXY_HOST,
          // Changes the origin of the host header to the target URL
          // changeOrigin: true,
          // secure: false,
          // Extra headers to be added to target requests
          headers: { 'Content-Type': 'application/json' },
          // configure: (proxy, options) => {
          //   // Emitted before the data is sent, allowing one to alter the
          //   // proxyReq request object.
          //   proxy.on('proxyReq', (proxyReq, req, res) => {
          //     console.info(`Proxy request: ${req.method} ${req.url}`);
          //     // console.log(res);
          //   });
          //   // Emitted if the request to the target got a response.
          //   proxy.on('proxyRes', (proxyRes, req, res) => {
          //     console.info(`Proxy response: ${proxyRes.statusCode} ${req.url}`);
          //   });
          //   // Emitted if the request to the target fail.
          //   proxy.on('error', (err, req, res) => {
          //     // res.writeHead(500, { 'Content-Type': 'text/plain' });
          //     // res.end(
          //     //   'Something went wrong. And we are reporting a custom error message.'
          //     // );
          //     // console.log('------------------');
          //     // console.log(res);
          //     // console.log('------------------');
          //     // console.log(res);
          //     // console.log('------------------');
          //   });
          // },
        },
      },
    },
  });
}
