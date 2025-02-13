import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, getUserInfo, setUserInfo, clearAuth } from '@/utils/auth'
import { resetRouter } from '@/router'

const getDefaultState = () => {
  const userInfo = getUserInfo()
  return {
    token: getToken(),
    name: userInfo?.name || '',
    avatar: userInfo?.avatar || '',
    roles: userInfo?.roles || [],
    permissions: userInfo?.permissions || []
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = Array.isArray(roles) ? roles : [roles].filter(Boolean)
  },
  SET_PERMISSIONS: (state, permissions) => {
    state.permissions = Array.isArray(permissions) ? permissions : [permissions].filter(Boolean)
  }
}

const actions = {
  // 用户登录
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password })
        .then(response => {
          const { token } = response
          commit('SET_TOKEN', token)
          setToken(token)
          resolve()
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  // 获取用户信息
  getInfo({ commit }) {
    return new Promise((resolve, reject) => {
      getInfo()
        .then(response => {
          const { role, name, avatar, permissions } = response

          if (!role) {
            reject(new Error('获取用户信息失败，请重新登录'))
            return
          }

          const roles = Array.isArray(role) ? role : [role].filter(Boolean)
          
          commit('SET_ROLES', roles)
          commit('SET_NAME', name)
          commit('SET_AVATAR', avatar)
          commit('SET_PERMISSIONS', permissions)

          // 保存用户信息到本地存储
          setUserInfo({
            name,
            avatar,
            roles,
            permissions
          })

          resolve({ roles, permissions })
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  // 用户登出
  logout({ commit }) {
    return new Promise((resolve, reject) => {
      logout()
        .then(() => {
          clearAuth()
          commit('RESET_STATE')
          resetRouter()
          resolve()
        })
        .catch(error => {
          reject(error)
        })
    })
  },

  // 重置 token
  resetToken({ commit }) {
    return new Promise(resolve => {
      clearAuth()
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
} 