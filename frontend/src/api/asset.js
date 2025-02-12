import request from '@/utils/request'

export function getAssetList(params) {
  return request({
    url: '/assets/',
    method: 'get',
    params
  })
}

export function getAssetStatistics() {
  return request({
    url: '/assets/statistics/',
    method: 'get'
  })
} 