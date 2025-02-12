import axios from 'axios'
import { ElMessage } from 'element-plus'
import store from '@/store'
import { getToken } from '@/utils/auth'
import router from '@/router'

// 创建axios实例
const service = axios.create({
  baseURL: '/api', // 使用 /api 前缀
  timeout: 5000 // 请求超时时间
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    if (store.state.user.token) {
      const token = getToken()
      if (token) {
        config.headers['Authorization'] = `Token ${token}`
      }
    }
    return config
  },
  error => {
    // 处理请求错误
    console.log(error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // Django REST framework 返回的数据直接使用
    return res
  },
  error => {
    console.log('Request Error:', {
      config: error.config,
      response: error.response,
      url: error.config?.url,
      method: error.config?.method,
      data: error.config?.data
    })
    // 如果是401错误，说明token失效，需要重新登录
    if (error.response?.status === 401) {
      store.dispatch('user/resetToken')
      router.push('/login')
    }
    ElMessage({
      message: error.response?.data?.detail || error.message || '请求失败',
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service 