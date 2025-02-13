<template>
  <div class="navbar">
    <div class="right-menu">
      <el-dropdown class="avatar-container" trigger="click">
        <div class="avatar-wrapper">
          <el-avatar 
            :size="32" 
            :src="avatar" 
            class="user-avatar"
          >
            {{ userInitials }}
          </el-avatar>
          <span class="user-name">{{ name }}</span>
          <el-icon class="el-icon-caret-bottom"><CaretBottom /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu class="user-dropdown">
            <router-link to="/profile">
              <el-dropdown-item>
                <el-icon><User /></el-icon>
                个人中心
              </el-dropdown-item>
            </router-link>
            <el-dropdown-item divided @click="handleLogout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { CaretBottom, User, SwitchButton } from '@element-plus/icons-vue'

export default {
  name: 'Navbar',
  components: {
    CaretBottom,
    User,
    SwitchButton
  },
  setup() {
    const store = useStore()
    const router = useRouter()

    const name = computed(() => store.state.user.name)
    const avatar = computed(() => store.state.user.avatar)
    const userInitials = computed(() => {
      const userName = store.state.user.name || ''
      return userName.charAt(0).toUpperCase()
    })

    const handleLogout = () => {
      ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        await store.dispatch('user/logout')
        router.push('/login')
      })
    }

    return {
      name,
      avatar,
      userInitials,
      handleLogout
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  padding: 0 16px;

  .right-menu {
    float: right;
    height: 100%;
    display: flex;
    align-items: center;

    .avatar-container {
      cursor: pointer;
      
      .avatar-wrapper {
        display: flex;
        align-items: center;
        padding: 5px 8px;
        border-radius: 4px;
        transition: background 0.3s;

        &:hover {
          background: rgba(0, 0, 0, 0.025);
        }

        .user-avatar {
          margin-right: 8px;
          background: #409EFF;
          color: #fff;
          font-weight: 600;
        }

        .user-name {
          font-size: 14px;
          color: #606266;
          margin-right: 8px;
        }

        .el-icon-caret-bottom {
          font-size: 12px;
          color: #909399;
        }
      }
    }
  }
}

:deep(.user-dropdown) {
  .el-dropdown-menu__item {
    padding: 8px 16px;
    display: flex;
    align-items: center;
    line-height: 1;

    .el-icon {
      margin-right: 8px;
      font-size: 16px;
    }
  }

  a {
    text-decoration: none;
    color: inherit;
  }
}

.el-dropdown-menu__item.is-divided {
  border-top: 1px solid #ebeef5;
  margin: 6px 0;
  padding-top: 12px;
}
</style> 