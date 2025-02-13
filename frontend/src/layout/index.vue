<template>
  <div class="app-wrapper">
    <sidebar class="sidebar-container" />
    <div class="main-container">
      <navbar />
      <app-main />
    </div>
  </div>
</template>

<script>
import { Navbar, Sidebar, AppMain } from './components'

export default {
  name: 'Layout',
  components: {
    Navbar,
    Sidebar,
    AppMain
  }
}
</script>

<style lang="scss" scoped>
.app-wrapper {
  position: relative;
  height: 100vh;
  width: 100%;
}

.main-container {
  min-height: 100%;
  margin-left: 210px;  // 与侧边栏宽度对应
  position: relative;
  background-color: #f0f2f5;
}

.sidebar-container {
  transition: width 0.28s;
}
</style> 