// import Layout from '@/views/layout/Layout.vue'
import { asyncRoutes, constantRoutes, allRoutes } from '@/router'
// import { getRoutes } from '@/api/role'

/**
 * 使用 meta.roles 判断当前用户是否有权限
 * @param roles
 * @param route
 */
function hasPermission(roles, route) {
  if (route.meta && route.meta.roles) {
    // 确保 roles 是数组并且有效
    const userRoles = Array.isArray(roles) ? roles : [roles].filter(Boolean)
    return userRoles.some(role => route.meta.roles.includes(role))
  }
  return true
}

/**
 * 递归过滤异步路由表
 * @param routes asyncRoutes
 * @param roles
 */
export function filterAsyncRoutes(routes, roles) {
  const res = []

  routes.forEach(route => {
    const tmp = { ...route }
    if (hasPermission(roles, tmp)) {
      if (tmp.children) {
        tmp.children = filterAsyncRoutes(tmp.children, roles)
      }
      res.push(tmp)
    }
  })

  return res
}

const state = {
  // 初始化时使用所有路由
  routes: allRoutes,
  addRoutes: asyncRoutes
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.addRoutes = routes
    state.routes = allRoutes
  },
  RESET_ROUTES: (state) => {
    state.addRoutes = []
    state.routes = constantRoutes
  }
}

const actions = {
  // eslint-disable-next-line no-unused-vars
  generateRoutes({ commit }, _roles) {
    return new Promise(resolve => {
      // 使用所有路由，权限由后端控制
      commit('SET_ROUTES', asyncRoutes)
      resolve(asyncRoutes)
    })
  },
  
  resetRoutes({ commit }) {
    commit('RESET_ROUTES')
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 