import Cookies from 'js-cookie'

const TokenKey = 'Admin-Token'
const UserInfoKey = 'User-Info'

// 获取token
export function getToken() {
  return localStorage.getItem(TokenKey)
}

// 设置token
export function setToken(token) {
  return localStorage.setItem(TokenKey, token)
}

// 移除token
export function removeToken() {
  return localStorage.removeItem(TokenKey)
}

// 获取用户信息
export function getUserInfo() {
  const info = localStorage.getItem(UserInfoKey)
  return info ? JSON.parse(info) : null
}

// 设置用户信息
export function setUserInfo(info) {
  return localStorage.setItem(UserInfoKey, JSON.stringify(info))
}

// 移除用户信息
export function removeUserInfo() {
  return localStorage.removeItem(UserInfoKey)
}

// 清除认证信息
export function clearAuth() {
  removeToken()
  removeUserInfo()
  Cookies.remove(TokenKey)
}

// 检查是否已登录
export function isAuthenticated() {
  return !!getToken()
}

// 设置token过期时间
export function setTokenWithExpiry(token, expiryHours = 24) {
  return Cookies.set(TokenKey, token, {
    expires: expiryHours / 24 // Cookies.set 接受天数作为过期时间
  })
}

// 获取token过期状态
export function isTokenExpired() {
  const token = getToken()
  if (!token) return true
  
  // 如果需要检查token的具体过期时间，可以解析JWT token
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp * 1000 < Date.now()
  } catch (e) {
    return true
  }
}

// 在现有的代码基础上添加以下函数
export function isValidToken() {
  const token = getToken()
  if (!token) return false

  // 如果需要验证token的有效性，可以在这里添加验证逻辑
  return true
}

export function initializeUserState(store) {
  const token = getToken()
  const userInfo = getUserInfo()

  if (token && userInfo) {
    store.commit('user/SET_TOKEN', token)
    store.commit('user/SET_NAME', userInfo.name)
    store.commit('user/SET_AVATAR', userInfo.avatar)
    store.commit('user/SET_ROLES', userInfo.roles)
    store.commit('user/SET_PERMISSIONS', userInfo.permissions)
    return true
  }
  return false
} 