import axios from 'axios'
import { ElMessage } from 'element-plus'
import store from '@/store'
import { getToken } from '@/utils/auth'
import router from '@/router'

// 创建 axios 实例
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API || 'http://localhost:8000/api',
  timeout: 5000,
  withCredentials: true
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const token = getToken()
    if (token) {
      // 修改 token 格式
      config.headers['Authorization'] = `Token ${token}`
    }
    return config
  },
  error => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('Error Response:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
      config: error.config
    })

    // 处理 401 错误
    if (error.response?.status === 401) {
      store.dispatch('user/resetToken')
      router.push('/login')
    }

    const message = error.response?.data?.error || error.message || '请求失败'
    ElMessage({
      message: message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service 