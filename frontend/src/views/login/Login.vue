<template>
  <div class="login-container">
    <el-form
      ref="loginFormRef"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      autocomplete="on"
    >
      <div class="title-container">
        <h3 class="title">资产管理系统</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <el-icon><User /></el-icon>
        </span>
        <el-input
          ref="usernameRef"
          v-model="loginForm.username"
          placeholder="请输入用户名"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
          clearable
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <el-icon><Lock /></el-icon>
        </span>
        <el-input
          :key="passwordType"
          ref="passwordRef"
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="请输入密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter="handleLogin"
        />
        <span class="show-pwd" @click="showPwd">
          <el-icon>
            <component :is="passwordType === 'password' ? 'Hide' : 'View'" />
          </el-icon>
        </span>
      </el-form-item>

      <el-button
        :loading="loading"
        type="primary"
        class="login-button"
        @click.prevent="handleLogin"
      >
        {{ loading ? '登录中...' : '登录' }}
      </el-button>
    </el-form>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, nextTick } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, View, Hide } from '@element-plus/icons-vue'

export default defineComponent({
  name: 'Login',
  components: { User, Lock, View, Hide },
  setup() {
    const store = useStore()
    const router = useRouter()
    const route = useRoute()

    const loginFormRef = ref(null)
    const usernameRef = ref(null)
    const passwordRef = ref(null)

    const loginForm = reactive({
      username: '',
      password: ''
    })

    const loginRules = {
      username: [
        { required: true, trigger: 'blur', message: '请输入用户名' },
        { min: 4, max: 20, message: '用户名长度在 4 到 20 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, trigger: 'blur', message: '请输入密码' },
        { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
      ]
    }

    const loading = ref(false)
    const passwordType = ref('password')

    const showPwd = () => {
      passwordType.value = passwordType.value === 'password' ? '' : 'password'
      nextTick(() => {
        passwordRef.value.focus()
      })
    }

    const handleLogin = () => {
      if (!loginFormRef.value) return
      
      loginFormRef.value.validate(async valid => {
        if (valid) {
          loading.value = true
          try {
            await store.dispatch('user/login', loginForm)
            const redirect = route.query.redirect || '/dashboard'
            router.replace(redirect)
            ElMessage.success('登录成功')
          } catch (error) {
            console.error('Login failed:', error)
            ElMessage.error(error.message || '登录失败，请检查用户名和密码')
          } finally {
            loading.value = false
          }
        }
      })
    }

    return {
      loginForm,
      loginFormRef,
      loginRules,
      loading,
      passwordType,
      showPwd,
      handleLogin,
      usernameRef,
      passwordRef
    }
  }
})
</script>

<style lang="scss" scoped>
$bg: #2d3a4b;
$cursor: #fff;
$dark-gray: #889aa4;
$light-gray: #eee;

.login-container {
  min-height: 100vh;
  width: 100%;
  background-color: $bg;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;

  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
    background: rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  }

  .title-container {
    position: relative;
    margin-bottom: 40px;
    text-align: center;

    .title {
      font-size: 26px;
      color: $light-gray;
      margin: 0;
      font-weight: bold;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark-gray;
    vertical-align: middle;
    display: inline-block;
    width: 30px;
    text-align: center;
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark-gray;
    cursor: pointer;
    user-select: none;
    transition: color 0.3s;

    &:hover {
      color: $light-gray;
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
    margin-bottom: 20px;

    &:hover {
      border-color: rgba(255, 255, 255, 0.2);
    }
  }

  .el-input {
    display: inline-block;
    height: 47px;
    width: calc(100% - 40px);

    input {
      background: transparent;
      border: 0;
      -webkit-appearance: none;
      border-radius: 0;
      padding: 12px 5px 12px 15px;
      color: $light-gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0 1000px $bg inset !important;
        -webkit-text-fill-color: $light-gray !important;
      }
    }
  }

  .login-button {
    width: 100%;
    margin-bottom: 30px;
    padding: 12px 15px;
    font-size: 16px;
    
    &:focus,
    &:hover {
      opacity: 0.9;
    }
  }
}

@media screen and (max-width: 520px) {
  .login-container {
    .login-form {
      padding: 100px 15px 0;
      margin: 0 20px;
    }
  }
}
</style> 