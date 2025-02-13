import request from '@/utils/request'

// 用户认证相关
export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data: {
      username: data.username,
      password: data.password
    }
  })
}

export function logout() {
  return request({
    url: '/users/logout/',
    method: 'post'
  })
}

export function getInfo() {
  return request({
    url: '/users/me/',
    method: 'get'
  })
}

// 用户管理相关
export function getUserList(params) {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}

export function getDevelopers() {
  return request({
    url: '/users/developers/',
    method: 'get'
  })
}

export function getManagers() {
  return request({
    url: '/users/managers/',
    method: 'get'
  })
}

export function createUser(data) {
  return request({
    url: '/users/',
    method: 'post',
    data
  })
}

export function updateUser(id, data) {
  return request({
    url: `/users/${id}/`,
    method: 'put',
    data
  })
}

export function deleteUser(id) {
  return request({
    url: `/users/${id}/`,
    method: 'delete'
  })
}

// 角色管理相关
export function getRoleList() {
  return request({
    url: '/roles/',
    method: 'get'
  })
}

export function createRole(data) {
  return request({
    url: '/roles/',
    method: 'post',
    data
  })
}

export function updateRole(id, data) {
  return request({
    url: `/roles/${id}/`,
    method: 'put',
    data
  })
}

export function deleteRole(id) {
  return request({
    url: `/roles/${id}/`,
    method: 'delete'
  })
}

// 权限管理相关
export function getPermissionList() {
  return request({
    url: '/permissions/',
    method: 'get'
  })
}

// 用户角色关联相关
export function assignRole(data) {
  return request({
    url: '/user-roles/',
    method: 'post',
    data
  })
}

export function removeRole(id) {
  return request({
    url: `/user-roles/${id}/`,
    method: 'delete'
  })
}

// 用户操作相关
export function changePassword(id, data) {
  return request({
    url: `/users/${id}/change_password/`,
    method: 'post',
    data
  })
}

export function lockUser(id, reason) {
  return request({
    url: `/users/${id}/lock/`,
    method: 'post',
    data: { reason }
  })
}

export function unlockUser(id) {
  return request({
    url: `/users/${id}/unlock/`,
    method: 'post'
  })
}

// 更新用户个人信息
export function updateUserProfile(data) {
  return request({
    url: '/api/users/profile/',
    method: 'put',
    data
  })
}

// 修改密码
export function updateUserPassword(data) {
  return request({
    url: '/api/users/change_password/',
    method: 'post',
    data
  })
} 