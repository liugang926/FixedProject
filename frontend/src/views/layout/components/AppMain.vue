<template>
  <section class="app-main">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <keep-alive :include="cachedViews || []">
          <component :is="Component" :key="$route.path" />
        </keep-alive>
      </transition>
    </router-view>
  </section>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'AppMain',
  setup() {
    const store = useStore()
    const cachedViews = computed(() => store.state.tagsView?.cachedViews || [])

    return {
      cachedViews
    }
  }
})
</script>

<style lang="scss" scoped>
.app-main {
  flex: 1;
  margin-top: 60px;
  padding: 20px;
  position: relative;
  overflow: auto;
  background-color: #f0f2f5;
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-thumb {
    background-color: rgba(144, 147, 153, 0.3);
    border-radius: 3px;
  }
  
  &::-webkit-scrollbar-track {
    background-color: transparent;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 