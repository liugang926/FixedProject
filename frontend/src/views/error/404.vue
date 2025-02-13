<template>
  <div class="error-page">
    <div class="error-code">404</div>
    <div class="error-desc">抱歉，你访问的页面不存在</div>
    <div class="error-handle">
      <el-button type="primary" @click="goBack">返回上一页</el-button>
      <el-button type="primary" @click="goHome">返回首页</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Page404',
  methods: {
    goBack() {
      this.$router.go(-1)
    },
    goHome() {
      this.$router.push('/')
    }
  }
}
</script>

<style lang="scss" scoped>
.error-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: #f3f3f3;
  
  .error-code {
    font-size: 160px;
    font-weight: 600;
    color: #1890ff;
  }
  
  .error-desc {
    font-size: 24px;
    color: #666;
    margin: 20px 0;
  }
  
  .error-handle {
    margin-top: 30px;
    
    .el-button {
      margin: 0 10px;
    }
  }
}
</style> 