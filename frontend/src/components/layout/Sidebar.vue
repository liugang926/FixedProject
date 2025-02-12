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
        :unique-opened="true"
        :collapse-transition="false"
        mode="vertical"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <sidebar-item
          v-for="route in routes"
          :key="route.path"
          :item="route"
          :base-path="route.path"
        />
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import SidebarItem from './SidebarItem.vue'
import * as ElementPlusIcons from '@element-plus/icons-vue'

export default defineComponent({
  name: 'Sidebar',
  components: {
    SidebarItem,
    ...ElementPlusIcons
  },
  setup() {
    const store = useStore()
    const route = useRoute()

    const routes = computed(() => store.state.permission.routes)
    const collapsed = computed(() => store.state.app.sidebarCollapsed)
    const activeMenu = computed(() => {
      const { meta, path } = route
      if (meta.activeMenu) {
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
    }
    
    .sidebar-logo {
      width: 32px;
      height: 32px;
    }
    
    .sidebar-title {
      margin-left: 10px;
      color: #fff;
      font-weight: 600;
      font-size: 16px;
      white-space: nowrap;
    }
  }

  .el-menu {
    border: none;
  }
}
</style> 