<template>
  <div class="sidebar-container">
    <div class="logo-container">
      <router-link to="/" class="logo-link">
        <h1 class="logo-title">资产管理系统</h1>
      </router-link>
    </div>
    <el-scrollbar wrap-class="scrollbar-wrapper">
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :background-color="variables.menuBg"
        :text-color="variables.menuText"
        :active-text-color="variables.menuActiveText"
        :unique-opened="true"
        :collapse-transition="false"
        mode="vertical"
        router
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
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from 'vuex'
import SidebarItem from './SidebarItem.vue'
import variables from '@/styles/variables.scss'

export default {
  name: 'Sidebar',
  components: { SidebarItem },
  setup() {
    const store = useStore()
    const route = useRoute()

    const routes = computed(() => store.state.permission.routes.filter(route => !route.hidden))
    const sidebar = computed(() => store.state.app.sidebar)
    
    const activeMenu = computed(() => {
      const { meta, path } = route
      if (meta?.activeMenu) {
        return meta.activeMenu
      }
      return path
    })

    const isCollapse = computed(() => !sidebar.value.opened)

    return {
      routes,
      activeMenu,
      isCollapse,
      variables
    }
  }
}
</script>

<style lang="scss" scoped>
@import "@/styles/variables.scss";

.sidebar-container {
  height: 100%;
  background-color: $menuBg;
  width: 210px;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 1001;
  transition: width 0.28s;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
  
  .logo-container {
    position: relative;
    height: 50px;
    padding: 10px 0;
    text-align: center;
    background-color: darken($menuBg, 2%);
    overflow: hidden;
    
    .logo-link {
      height: 100%;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;

      .logo-title {
        color: $menuText;
        font-size: 18px;
        font-weight: 600;
        margin: 0;
        white-space: nowrap;
        transition: color 0.3s;
        letter-spacing: 0.5px;
        text-shadow: 0 0 10px rgba(0, 0, 0, 0.3);

        &:hover {
          color: $menuActiveText;
        }
      }
    }

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 90%;
      height: 1px;
      background: linear-gradient(90deg, 
        transparent, 
        rgba(255, 255, 255, 0.2),
        transparent
      );
    }
  }

  .el-scrollbar {
    height: calc(100% - 50px);
    background-color: $menuBg;

    ::v-deep(.scrollbar-wrapper) {
      overflow-x: hidden !important;

      .el-scrollbar__view {
        height: 100%;
      }

      .el-scrollbar__bar.is-horizontal {
        display: none;
      }
    }
  }

  .el-menu {
    border: none;
    width: 100%;
    height: 100%;
    background-color: transparent;
  }

  ::v-deep(.el-sub-menu) {
    &.is-active {
      > .el-sub-menu__title {
        color: $menuActiveText !important;
        
        &::before {
          content: '';
          position: absolute;
          left: 0;
          top: 0;
          bottom: 0;
          width: 3px;
          background: $menuActiveText;
          opacity: 0.5;
        }
      }
    }

    .el-sub-menu__title {
      position: relative;
      color: $menuText !important;
      padding-left: 20px !important;
      transition: all 0.3s;

      &:hover {
        background-color: rgba(255, 255, 255, 0.04) !important;
        color: $menuActiveText !important;
      }

      i {
        color: inherit;
      }
    }

    // 子菜单样式
    .el-menu {
      background-color: darken($menuBg, 3%) !important;
      
      .el-menu-item {
        padding-left: 40px !important;
        background-color: transparent !important;
        
        &::before {
          left: -3px;
          opacity: 0;
          transition: all 0.3s;
        }

        &:hover::before {
          opacity: 0.2;
        }

        &.is-active::before {
          opacity: 1;
        }
      }
    }
  }

  ::v-deep(.el-menu-item) {
    position: relative;
    color: $menuText !important;
    background-color: transparent !important;
    transition: all 0.3s;

    &:hover {
      color: $menuActiveText !important;
      background-color: rgba(255, 255, 255, 0.04) !important;
    }

    &.is-active {
      color: $menuActiveText !important;
      background-color: rgba(255, 255, 255, 0.05) !important;

      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: $menuActiveText;
        box-shadow: 0 0 8px rgba(24, 144, 255, 0.5);
      }
    }
  }

  // 图标样式优化
  ::v-deep(.el-menu-item), ::v-deep(.el-sub-menu__title) {
    .el-icon {
      width: 24px;
      margin-right: 16px;
      font-size: 18px;
      vertical-align: middle;
      transition: transform 0.3s;
    }

    span {
      vertical-align: middle;
      font-size: 14px;
      transition: transform 0.3s;
    }

    &:hover {
      .el-icon, span {
        transform: translateX(3px);
      }
    }
  }

  // 折叠菜单时的样式
  &.is-collapse {
    width: 64px;
    
    .logo-title {
      display: none;
    }

    .el-menu-item, .el-sub-menu__title {
      padding-left: 20px !important;
    }
  }
}
</style> 