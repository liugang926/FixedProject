<template>
  <section class="app-main">
    <router-view v-slot="{ Component }">
      <transition name="fade-transform" mode="out-in">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </transition>
    </router-view>
  </section>
</template>

<script>
export default {
  name: 'AppMain'
}
</script>

<style lang="scss" scoped>
.app-main {
  min-height: calc(100vh - 50px);  // 减去导航栏高度
  padding: 20px;
  margin-top: 50px;  // 为导航栏留出空间
  position: relative;
  overflow: auto;
  box-sizing: border-box;
  background-color: #f0f2f5;
}

.fixed-header + .app-main {
  padding-top: 50px;
}

.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.5s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style> 