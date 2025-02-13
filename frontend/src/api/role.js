import request from '@/utils/request'

export function getRoleList() {
  return request({
    url: '/users/roles/',
    method: 'get'
  })
}

export function getPermissionList() {
  return request({
    url: '/users/permissions/',
    method: 'get'
  })
}

export function getRoleDetail(id) {
  return request({
    url: `/users/roles/${id}/`,
    method: 'get'
  })
}

export function createRole(data) {
  return request({
    url: '/users/roles/',
    method: 'post',
    data
  })
}

export function updateRole(id, data) {
  return request({
    url: `/users/roles/${id}/`,
    method: 'put',
    data
  })
}

export function deleteRole(id) {
  return request({
    url: `/users/roles/${id}/`,
    method: 'delete'
  })
} 