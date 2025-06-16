import request from './request'

// 获取文章列表（示例 API）
export function fetchPosts() {
  return request.get('/posts')
}
