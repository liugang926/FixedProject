const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    },
    client: {
      webSocketURL: {
        hostname: 'localhost',
        pathname: '/ws',
        port: 8080,
        protocol: 'ws',
      },
      logging: 'none',
      overlay: false
    },
    webSocketServer: false,
    historyApiFallback: true
  },
  configureWebpack: {
    performance: {
      hints: false
    },
    devServer: {
      historyApiFallback: true
    },
    define: {
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
      __VUE_OPTIONS_API__: true,
      __VUE_PROD_DEVTOOLS__: false
    }
  },
  publicPath: '/',
  css: {
    loaderOptions: {
      scss: {
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  }
}) 