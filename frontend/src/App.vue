<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <sidebar />
    </el-aside>
    <el-container>
      <el-header>
        <navbar />
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { defineComponent } from 'vue'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'

export default defineComponent({
  name: 'App',
  components: {
    Navbar,
    Sidebar
  }
})
</script>

<style lang="scss">
.layout-container {
  height: 100vh;
  
  .el-header {
    background-color: #fff;
    border-bottom: 1px solid #dcdfe6;
    padding: 0 20px;
  }
  
  .el-aside {
    background-color: #304156;
    color: #fff;
  }
  
  .el-main {
    background-color: #f0f2f5;
    padding: 20px;
  }
}
</style> 