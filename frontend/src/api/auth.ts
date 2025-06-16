import request from './request'
//axios 添加 JWT 登录请求方法
//这一行代码是 向后端 Django 的 JWT 接口 /api/token/ 发起 POST 请求，传入用户名密码，后端验证通过就返回一个 token 对象
export function login(data: { username: string; password: string }) {
  return request.post('/token/', data)
}

// axios 添加注册请求方法
// 向后端 Django 的注册接口 /api/register/ 发起 POST 请求，传入用户注册信息
export function register(data: { 
  username: string; 
  email: string; 
  password: string; 
  confirmPassword: string;
  firstName?: string;
  lastName?: string;
}) {
  return request.post('/register/', data)
}
