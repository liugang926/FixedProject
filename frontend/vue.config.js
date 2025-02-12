module.exports = {
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').join(__dirname, 'src')
      }
    }
  },
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
} 