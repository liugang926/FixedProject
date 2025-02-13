import router from './router'
import store from './store'
import { ElMessage } from 'element-plus'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { getToken, getUserInfo } from '@/utils/auth'
import getPageTitle from '@/utils/get-page-title'

NProgress.configure({ showSpinner: false })

const whiteList = ['/login']

router.beforeEach(async (to, from, next) => {
  NProgress.start()

  // 设置页面标题
  document.title = getPageTitle(to.meta.title)

  const hasToken = getToken()
  const userInfo = getUserInfo()

  if (hasToken) {
    if (to.path === '/login') {
      next({ path: '/' })
      NProgress.done()
    } else {
      try {
        // 检查是否已有用户角色信息
        const hasRoles = store.state.user.roles && store.state.user.roles.length > 0
        
        if (hasRoles) {
          // 检查路由是否已经添加
          if (to.matched.length === 0) {
            // 重新生成路由
            const accessRoutes = await store.dispatch('permission/generateRoutes', store.state.user.roles)
            // 添加路由
            accessRoutes.forEach(route => {
              router.addRoute(route)
            })
            // 重新导航到目标路由
            next({ ...to, replace: true })
          } else {
            next()
          }
        } else if (userInfo && userInfo.roles) {
          // 从本地存储恢复用户信息
          const { roles, name, avatar, permissions } = userInfo
          
          // 更新 store 中的用户信息
          store.commit('user/SET_ROLES', roles)
          store.commit('user/SET_NAME', name)
          store.commit('user/SET_AVATAR', avatar)
          store.commit('user/SET_PERMISSIONS', permissions)
          
          // 生成路由
          await store.dispatch('permission/generateRoutes', roles)
          
          // 重新导航
          next({ ...to, replace: true })
        } else {
          // 获取用户信息
          const { roles } = await store.dispatch('user/getInfo')
          
          // 生成路由
          await store.dispatch('permission/generateRoutes', roles)
          
          // 重新导航
          next({ ...to, replace: true })
        }
      } catch (error) {
        console.error('Permission error:', error)
        // 发生错误时重置令牌并重新登录
        await store.dispatch('user/resetToken')
        ElMessage.error(error.message || '出现错误，请重新登录')
        next(`/login?redirect=${to.path}`)
        NProgress.done()
      }
    }
  } else {
    if (whiteList.includes(to.path)) {
      next()
    } else {
      next(`/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  NProgress.done()
}) 