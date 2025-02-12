<template>
  <div class="app-wrapper" :class="{'hide-sidebar': collapsed}">
    <sidebar class="sidebar-container" />
    <div class="main-container">
      <div class="fixed-header">
        <navbar />
      </div>
      <app-main />
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { Navbar, Sidebar } from '@/components/layout'
import AppMain from './components/AppMain.vue'

export default defineComponent({
  name: 'Layout',
  components: {
    Navbar,
    Sidebar,
    AppMain
  }
})
</script>

<style lang="scss" scoped>
.app-wrapper {
  position: relative;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  
  .sidebar-container {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: 200px;
    transition: width 0.3s;
    z-index: 1001;
    overflow: hidden;
  }
  
  .main-container {
    min-height: 100%;
    margin-left: 200px;
    position: relative;
    transition: margin-left 0.3s;
    display: flex;
    flex-direction: column;
    background-color: #f0f2f5;
    
    .fixed-header {
      position: fixed;
      top: 0;
      right: 0;
      z-index: 1000;
      width: calc(100% - 200px);
      transition: width 0.3s;
      background-color: #fff;
      box-shadow: 0 1px 4px rgba(0,21,41,.08);
    }
  }
  
  &.hide-sidebar {
    .sidebar-container {
      width: 54px;
    }
    
    .main-container {
      margin-left: 54px;
      
      .fixed-header {
        width: calc(100% - 54px);
      }
    }
  }
}
</style> 