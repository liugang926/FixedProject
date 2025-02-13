<template>
  <div class="login-container">
    <el-form
      ref="loginForm"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      autocomplete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">系统登录</h3>
      </div>

      <el-form-item prop="username">
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="用户名"
          name="username"
          type="text"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <el-input
          ref="password"
          v-model="loginForm.password"
          placeholder="密码"
          name="password"
          :type="passwordType"
          autocomplete="on"
          @keyup.enter="handleLogin"
        />
      </el-form-item>

      <el-button
        :loading="loading"
        type="primary"
        style="width: 100%; margin-bottom: 30px"
        @click.prevent="handleLogin"
      >
        登录
      </el-button>
    </el-form>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      },
      passwordType: 'password',
      loading: false,
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    async handleLogin() {
      try {
        await this.$refs.loginForm.validate()
        this.loading = true
        
        // 登录
        await this.$store.dispatch('user/login', this.loginForm)
        
        // 获取用户信息
        const { role } = await this.$store.dispatch('user/getInfo')
        
        // 生成路由
        const accessRoutes = await this.$store.dispatch('permission/generateRoutes', { 
          roles: [role]
        })
        
        // 动态添加路由
        accessRoutes.forEach(route => {
          this.$router.addRoute(route)
        })

        // 跳转到首页或重定向页面
        await this.$router.push(this.redirect || '/')
      } catch (error) {
        console.error('Login error:', error)
        ElMessage.error(error.message || '登录失败')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100%;
  width: 100%;
  background-color: #2d3a4b;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-form {
  width: 520px;
  max-width: 100%;
  padding: 160px 35px 0;
  margin: 0 auto;
  overflow: hidden;
}

.title-container {
  position: relative;
  .title {
    font-size: 26px;
    color: #eee;
    margin: 0 auto 40px auto;
    text-align: center;
    font-weight: bold;
  }
}
</style> 