<template>
  <div class="sidebar-container">
    <div class="logo-container">
      <router-link to="/">
        <el-icon :size="32"><Monitor /></el-icon>
        <span class="sidebar-title" v-if="!collapsed">固定资产管理系统</span>
      </router-link>
    </div>
    
    <el-scrollbar>
      <el-menu
        :default-active="activeMenu"
        :collapse="collapsed"
        :unique-opened="false"
        :collapse-transition="false"
        mode="vertical"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <template v-for="route in routes" :key="route.path">
          <template v-if="!route.hidden">
            <el-menu-item v-if="!route.children || route.children.length === 0" :index="route.path">
              <el-icon><component :is="route.meta?.icon" /></el-icon>
              <template #title>{{ route.meta?.title }}</template>
            </el-menu-item>

            <template v-else>
              <el-menu-item v-if="route.children.length === 1" :index="`${route.path}/${route.children[0].path}`">
                <el-icon><component :is="route.children[0].meta?.icon" /></el-icon>
                <template #title>{{ route.children[0].meta?.title }}</template>
              </el-menu-item>

              <el-sub-menu v-else :index="route.path">
                <template #title>
                  <el-icon><component :is="route.meta?.icon" /></el-icon>
                  <span>{{ route.meta?.title }}</span>
                </template>
                <el-menu-item v-for="child in route.children" :key="child.path" :index="`${route.path}/${child.path}`">
                  <el-icon><component :is="child.meta?.icon" /></el-icon>
                  <template #title>{{ child.meta?.title }}</template>
                </el-menu-item>
              </el-sub-menu>
            </template>
          </template>
        </template>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import * as ElementPlusIcons from '@element-plus/icons-vue'

export default defineComponent({
  name: 'Sidebar',
  components: {
    ...ElementPlusIcons
  },
  setup() {
    const store = useStore()
    const route = useRoute()

    const routes = computed(() => {
      return store.state.permission.routes
    })
    
    const collapsed = computed(() => store.state.app.sidebarCollapsed || false)
    
    const activeMenu = computed(() => {
      const { meta, path } = route
      if (meta?.activeMenu) {
        return meta.activeMenu
      }
      return path
    })

    return {
      routes,
      collapsed,
      activeMenu
    }
  }
})
</script>

<style lang="scss" scoped>
.sidebar-container {
  height: 100%;
  background-color: #304156;
  
  .logo-container {
    height: 60px;
    padding: 10px;
    text-align: center;
    
    a {
      text-decoration: none;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
    }
    
    .sidebar-title {
      margin-left: 10px;
      font-weight: 600;
      font-size: 16px;
      white-space: nowrap;
    }
  }

  .el-scrollbar {
    height: calc(100% - 60px);
  }

  .el-menu {
    border: none;
    height: 100%;
    width: 100% !important;
  }

  .el-menu-item, .el-sub-menu__title {
    .el-icon {
      margin-right: 16px;
      width: 24px;
      text-align: center;
    }
  }
}
</style> 