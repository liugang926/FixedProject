<template>
  <div v-if="!item.hidden">
    <!-- 没有子路由的情况 -->
    <template v-if="!hasChildren(item)">
      <el-menu-item 
        :index="resolvePath(item.path)"
        :class="{'submenu-title-noDropdown': !isNest}"
      >
        <el-icon v-if="item.meta && item.meta.icon">
          <component :is="item.meta.icon" />
        </el-icon>
        <template #title>
          <span v-if="item.meta">{{ item.meta.title }}</span>
        </template>
      </el-menu-item>
    </template>

    <!-- 有子路由的情况 -->
    <el-sub-menu 
      v-else 
      :index="resolvePath(item.path)"
      popper-append-to-body
    >
      <template #title>
        <el-icon v-if="item.meta && item.meta.icon">
          <component :is="item.meta.icon" />
        </el-icon>
        <span v-if="item.meta">{{ item.meta.title }}</span>
      </template>
      <sidebar-item
        v-for="child in item.children"
        :key="child.path"
        :item="child"
        :base-path="resolvePath(item.path)"
        :is-nest="true"
      />
    </el-sub-menu>
  </div>
</template>

<script>
import path from 'path-browserify'

export default {
  name: 'SidebarItem',
  props: {
    item: {
      type: Object,
      required: true
    },
    basePath: {
      type: String,
      default: ''
    },
    isNest: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    hasChildren(item) {
      return item.children && item.children.length > 0
    },
    resolvePath(routePath) {
      if (!routePath) return ''
      if (/^(https?:|mailto:|tel:)/.test(routePath)) {
        return routePath
      }
      return path.resolve(this.basePath, routePath)
    }
  }
}
</script>

<style lang="scss" scoped>
.el-menu-item, .el-sub-menu {
  .el-icon {
    margin-right: 16px;
    vertical-align: middle;
    width: 24px;
    text-align: center;
  }
  
  .el-sub-menu__icon-arrow {
    margin-right: 0;
  }
}
</style> 