import Cookies from 'js-cookie'

const TokenKey = 'Asset_Management_Token'
const TokenExpireKey = 'Asset_Management_Token_Expire'

// 获取token
export function getToken() {
  const token = Cookies.get(TokenKey)
  const expireTime = Cookies.get(TokenExpireKey)
  if (token && expireTime && new Date().getTime() < parseInt(expireTime)) {
    return token
  }
  // token 过期或不存在，清除
  removeToken()
  return null
}

// 设置token
export function setToken(token) {
  // 设置24小时过期
  const expire = new Date().getTime() + 24 * 60 * 60 * 1000
  Cookies.set(TokenKey, token)
  Cookies.set(TokenExpireKey, expire.toString())
}

// 移除token
export function removeToken() {
  Cookies.remove(TokenKey)
  Cookies.remove(TokenExpireKey)
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