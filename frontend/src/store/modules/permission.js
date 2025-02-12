const state = {
  routes: []
}

const mutations = {
  SET_ROUTES: (state, routes) => {
    state.routes = routes
  }
}

const actions = {
  generateRoutes({ commit }) {
    return new Promise(resolve => {
      // 这里可以根据用户角色动态生成路由
      const accessedRoutes = [
        {
          path: '/dashboard',
          name: 'Dashboard',
          meta: { title: '仪表盘', icon: 'Menu', roles: ['admin', 'user'] }
        },
        {
          path: '/assets',
          name: 'Assets',
          meta: { title: '资产管理', icon: 'Document', roles: ['admin', 'user'] }
        },
        {
          path: '/users',
          name: 'Users',
          meta: { title: '用户管理', icon: 'User', roles: ['admin'] }
        }
      ]
      commit('SET_ROUTES', accessedRoutes)
      resolve(accessedRoutes)
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 