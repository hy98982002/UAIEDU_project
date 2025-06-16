import request from './request'

/**
 * 获取课程列表
 * 需要JWT认证
 */
export function getCourses() {
  return request.get('/courses/')
}

/**
 * 测试无认证访问
 */
export function getCoursesWithoutAuth() {
  // 临时移除token进行测试
  const originalGet = request.get
  return originalGet('/courses/', {
    headers: {
      Authorization: '' // 清空认证头
    }
  })
} 