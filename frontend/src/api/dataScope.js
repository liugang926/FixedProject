import request from '@/utils/request'

export function getDataScope(roleId) {
  return request({
    url: `/data-scopes/${roleId}/`,
    method: 'get'
  })
}

export function updateDataScope(roleId, data) {
  return request({
    url: `/data-scopes/${roleId}/`,
    method: 'put',
    data
  })
}

export function getDepartmentTree() {
  return request({
    url: '/departments/tree/',
    method: 'get'
  })
} 