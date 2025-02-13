<template>
  <div class="app-container">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
            </div>
          </template>
          <div class="text-center">
            <el-avatar :size="100" :src="user.avatar">
              {{ userInitials }}
            </el-avatar>
            <h2>{{ user.name }}</h2>
            <p>{{ user.role }}</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="18">
        <el-card>
          <template #header>
            <el-tabs v-model="activeTab">
              <el-tab-pane label="基本信息" name="basic">
                <el-form
                  ref="basicForm"
                  :model="userForm"
                  :rules="rules"
                  label-width="100px"
                >
                  <el-form-item label="用户名" prop="username">
                    <el-input v-model="userForm.username" disabled />
                  </el-form-item>
                  <el-form-item label="姓名" prop="name">
                    <el-input v-model="userForm.name" />
                  </el-form-item>
                  <el-form-item label="邮箱" prop="email">
                    <el-input v-model="userForm.email" />
                  </el-form-item>
                  <el-form-item label="手机号" prop="phone">
                    <el-input v-model="userForm.phone" />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="updateBasicInfo">保存修改</el-button>
                  </el-form-item>
                </el-form>
              </el-tab-pane>
              <el-tab-pane label="修改密码" name="password">
                <el-form
                  ref="pwdForm"
                  :model="passwordData"
                  :rules="passwordRules"
                  label-width="100px"
                >
                  <el-form-item label="当前密码" prop="oldPassword">
                    <el-input
                      v-model="passwordData.oldPassword"
                      type="password"
                      show-password
                    />
                  </el-form-item>
                  <el-form-item label="新密码" prop="newPassword">
                    <el-input
                      v-model="passwordData.newPassword"
                      type="password"
                      show-password
                    />
                  </el-form-item>
                  <el-form-item label="确认新密码" prop="confirmPassword">
                    <el-input
                      v-model="passwordData.confirmPassword"
                      type="password"
                      show-password
                    />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="updatePassword">修改密码</el-button>
                  </el-form-item>
                </el-form>
              </el-tab-pane>
            </el-tabs>
          </template>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { updateUserProfile, updateUserPassword } from '@/api/user'

export default {
  name: 'Profile',
  setup() {
    const store = useStore()
    const basicForm = ref(null)
    const pwdForm = ref(null)
    const activeTab = ref('basic')

    const user = computed(() => ({
      name: store.state.user.name,
      avatar: store.state.user.avatar,
      role: store.state.user.roles[0]
    }))

    const userInitials = computed(() => {
      const name = store.state.user.name || ''
      return name.charAt(0).toUpperCase()
    })

    const userForm = reactive({
      username: store.state.user.name,
      name: store.state.user.name,
      email: '',
      phone: ''
    })

    const passwordData = reactive({
      oldPassword: '',
      newPassword: '',
      confirmPassword: ''
    })

    const rules = {
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
      ]
    }

    const passwordRules = {
      oldPassword: [
        { required: true, message: '请输入当前密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
      ],
      newPassword: [
        { required: true, message: '请输入新密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, message: '请再次输入新密码', trigger: 'blur' },
        {
          validator: (rule, value, callback) => {
            if (value !== passwordData.newPassword) {
              callback(new Error('两次输入密码不一致'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ]
    }

    const updateBasicInfo = () => {
      basicForm.value.validate(async (valid) => {
        if (valid) {
          try {
            await updateUserProfile(userForm)
            ElMessage.success('个人信息更新成功')
            // 更新store中的用户信息
            store.commit('user/SET_NAME', userForm.name)
          } catch (error) {
            console.error('更新个人信息失败:', error)
            ElMessage.error('更新失败，请重试')
          }
        }
      })
    }

    const updatePassword = () => {
      pwdForm.value.validate(async (valid) => {
        if (valid) {
          try {
            await updateUserPassword({
              oldPassword: passwordData.oldPassword,
              newPassword: passwordData.newPassword
            })
            ElMessage.success('密码修改成功，请重新登录')
            // 退出登录
            await store.dispatch('user/logout')
          } catch (error) {
            console.error('修改密码失败:', error)
            ElMessage.error('修改失败，请重试')
          }
        }
      })
    }

    return {
      user,
      userInitials,
      activeTab,
      userForm,
      passwordData,
      rules,
      passwordRules,
      basicForm,
      pwdForm,
      updateBasicInfo,
      updatePassword
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  padding: 20px;
}

.text-center {
  text-align: center;
}

.box-card {
  .el-avatar {
    margin-bottom: 20px;
    background: #409EFF;
  }

  h2 {
    margin: 10px 0;
    font-size: 18px;
  }

  p {
    color: #666;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.el-tabs__nav) {
  float: left;
  margin-bottom: 15px;
}
</style> 