<template>
  <div class="app-wrapper">
    <sidebar class="sidebar-container" />
    <div class="main-container">
      <navbar />
      <div class="app-main">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { Navbar, Sidebar } from '@/components/layout'

export default defineComponent({
  name: 'Layout',
  components: {
    Navbar,
    Sidebar
  }
})
</script>

<style lang="scss" scoped>
.app-wrapper {
  position: relative;
  height: 100vh;
  width: 100%;
  
  .sidebar-container {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: 200px;
    z-index: 1001;
    background-color: #304156;
    transition: width 0.3s;
  }
  
  .main-container {
    min-height: 100%;
    margin-left: 200px;
    position: relative;
    
    .app-main {
      padding: 20px;
      min-height: calc(100vh - 60px);
      margin-top: 60px;
      background-color: #f0f2f5;
    }
  }
}
</style> 