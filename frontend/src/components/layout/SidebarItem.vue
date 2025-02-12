<template>
  <div v-if="!item.hidden">
    <!-- 没有子菜单的情况 -->
    <template v-if="!hasChildren(item)">
      <el-menu-item :index="resolvePath(item.path)" @click="handleLink(item)">
        <el-icon v-if="item.meta && item.meta.icon">
          <component :is="toIcon(item.meta.icon)" />
        </el-icon>
        <template #title>
          <span>{{ item.meta.title }}</span>
        </template>
      </el-menu-item>
    </template>

    <!-- 有子菜单的情况 -->
    <el-sub-menu v-else :index="resolvePath(item.path)">
      <template #title>
        <el-icon v-if="item.meta && item.meta.icon">
          <component :is="item.meta.icon" />
        </el-icon>
        <span>{{ item.meta.title }}</span>
      </template>
      
      <sidebar-item
        v-for="child in item.children"
        :key="child.path"
        :item="child"
        :base-path="resolvePath(item.path)"
      />
    </el-sub-menu>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import path from 'path-browserify'

export default defineComponent({
  name: 'SidebarItem',
  props: {
    item: {
      type: Object,
      required: true
    },
    basePath: {
      type: String,
      default: ''
    }
  },
  setup(props) {
    const router = useRouter()

    const hasChildren = (route) => {
      return route.children && route.children.length > 0
    }

    const resolvePath = (routePath) => {
      return path.resolve(props.basePath, routePath)
    }

    const handleLink = (item) => {
      const { path } = item
      router.push(resolvePath(path))
    }

    const toIcon = (icon) => {
      if (!icon) return ''
      // 移除 'el-icon-' 前缀，并将首字母大写
      return icon.replace('el-icon-', '')
        .split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join('')
    }

    return {
      hasChildren,
      resolvePath,
      handleLink,
      toIcon
    }
  }
})
</script> 