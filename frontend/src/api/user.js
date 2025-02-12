import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/auth-token/',
    method: 'post',
    data: {  // 确保数据格式正确
      username: data.username,
      password: data.password
    }
  })
}

export function getInfo() {
  return request({
    url: '/users/me/',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/users/logout/',
    method: 'post'
  })
}

export function getUserList(params) {
  return request({
    url: '/users/',
    method: 'get',
    params
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

export function lockUser(id, reason) {
  return request({
    url: `/users/${id}/lock/`,
    method: 'post',
    data: { reason }
  })
}

export function unlockUser(id, reason) {
  return request({
    url: `/users/${id}/unlock/`,
    method: 'post',
    data: { reason }
  })
} 