<template>
  <div class="navbar">
    <div class="left-menu">
      <el-button type="text" @click="toggleSidebar">
        <el-icon><Fold v-if="!collapsed" /><Expand v-else /></el-icon>
      </el-button>
      <breadcrumb class="breadcrumb-container" />
    </div>
    
    <div class="right-menu">
      <el-dropdown trigger="click">
        <div class="avatar-wrapper">
          <el-avatar :size="30" :src="userAvatar">{{ userInitials }}</el-avatar>
          <span class="user-name">{{ userName }}</span>
          <el-icon><CaretBottom /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleProfile">个人信息</el-dropdown-item>
            <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { Fold, Expand, CaretBottom } from '@element-plus/icons-vue'
import Breadcrumb from './Breadcrumb.vue'

export default defineComponent({
  name: 'Navbar',
  components: {
    Breadcrumb,
    Fold,
    Expand,
    CaretBottom
  },
  setup() {
    const store = useStore()
    const router = useRouter()

    const userName = computed(() => store.state.user.name || '用户')
    const userAvatar = computed(() => store.state.user.avatar)
    const userInitials = computed(() => userName.value.charAt(0).toUpperCase())
    const collapsed = computed(() => store.state.app.sidebarCollapsed)

    const toggleSidebar = () => {
      store.commit('app/TOGGLE_SIDEBAR')
    }

    const handleProfile = () => {
      router.push('/profile')
    }

    const handleLogout = async () => {
      await store.dispatch('user/logout')
      router.push('/login')
    }

    return {
      userName,
      userAvatar,
      userInitials,
      collapsed,
      toggleSidebar,
      handleProfile,
      handleLogout
    }
  }
})
</script>

<style lang="scss" scoped>
.navbar {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;

  .left-menu {
    display: flex;
    align-items: center;
    
    .breadcrumb-container {
      margin-left: 15px;
    }
  }

  .right-menu {
    margin-right: 20px;

    .avatar-wrapper {
      display: flex;
      align-items: center;
      cursor: pointer;
      
      .user-name {
        margin: 0 8px;
        color: #606266;
      }
    }
  }
}
</style> 