import request from '@/utils/request'

export function getOperationLogs(params) {
  return request({
    url: '/operation-logs/',
    method: 'get',
    params
  })
}

export function getOperationLogStats(params) {
  return request({
    url: '/operation-logs/statistics/',
    method: 'get',
    params
  })
}

export function exportOperationLogs(params) {
  return request({
    url: '/operation-logs/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
} 