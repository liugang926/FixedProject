<template>
  <div class="login-container">
    <el-button @click="testApi" type="text">测试API</el-button>
    <el-form
      ref="loginFormRef"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      autocomplete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">固定资产管理系统</h3>
      </div>

      <el-form-item prop="username">
        <el-input
          v-model="loginForm.username"
          placeholder="用户名"
          type="text"
          tabindex="1"
          autocomplete="on"
        >
          <template #prefix>
            <el-icon><User /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item prop="password">
        <el-input
          v-model="loginForm.password"
          :type="passwordVisible ? 'text' : 'password'"
          placeholder="密码"
          tabindex="2"
          autocomplete="on"
          @keyup.enter="handleLogin"
        >
          <template #prefix>
            <el-icon><Lock /></el-icon>
          </template>
          <template #suffix>
            <el-icon 
              class="password-icon" 
              @click="passwordVisible = !passwordVisible"
            >
              <View v-if="passwordVisible" />
              <Hide v-else />
            </el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-button
        :loading="loading"
        type="primary"
        class="login-button"
        @click="handleLogin"
      >
        登录
      </el-button>
    </el-form>
  </div>
</template>

<script>
import { defineComponent, ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, View, Hide } from '@element-plus/icons-vue'
import request from '@/utils/request'

export default defineComponent({
  name: 'Login',
  components: {
    User,
    Lock,
    View,
    Hide
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()
    const loginFormRef = ref(null)
    const loading = ref(false)
    const passwordVisible = ref(false)

    const loginForm = reactive({
      username: '',
      password: ''
    })

    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, message: '用户名长度至少为3个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
      ]
    }

    const handleLogin = () => {
      loginFormRef.value?.validate(async (valid) => {
        if (valid) {
          try {
            loading.value = true
            await store.dispatch('user/login', {
              username: loginForm.username,
              password: loginForm.password
            })
            await store.dispatch('permission/generateRoutes')
            ElMessage.success('登录成功')
            const redirect = route.query.redirect || '/'
            router.push({ path: redirect })
          } catch (error) {
            ElMessage.error(error.message || '登录失败')
          } finally {
            loading.value = false
          }
        }
      })
    }

    const testApi = async () => {
      try {
        const res = await request({
          url: '/debug/',
          method: 'get'
        })
        console.log('Debug API response:', res)
      } catch (error) {
        console.log('Debug API error:', error)
      }
    }

    return {
      loginForm,
      loginRules,
      loginFormRef,
      loading,
      passwordVisible,
      handleLogin,
      testApi
    }
  }
})
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  width: 100%;
  background-color: #2d3a4b;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;

  .login-form {
    width: 400px;
    padding: 40px 35px;
    background: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);

    .title-container {
      text-align: center;
      margin-bottom: 30px;

      .title {
        font-size: 26px;
        color: #333;
        margin: 0;
      }
    }

    :deep(.el-input) {
      height: 48px;
      
      input {
        height: 48px;
        padding-left: 40px;
        background: transparent;
        
        &:-webkit-autofill {
          box-shadow: 0 0 0 1000px #fff inset !important;
        }
      }

      .el-input__prefix {
        left: 10px;
        top: 0;
        height: 100%;
        color: #909399;
      }
    }

    .password-icon {
      cursor: pointer;
      color: #909399;
    }

    .login-button {
      width: 100%;
      height: 48px;
      margin-top: 10px;
    }
  }
}
</style> 