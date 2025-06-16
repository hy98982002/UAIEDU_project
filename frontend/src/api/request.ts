import axios from 'axios'
/* baseURL: 'http://localhost:8000/api'
这是设置所有请求的“基础地址”。也就是说：

以后你只需要写 /courses/，Axios 会自动拼接成：

http://localhost:8000/api/courses/
非常适合前后端分离项目中，前端调用后端接口的情况。

一旦部署到线上，只需把 baseURL 改成如：

baseURL: 'https://www.uaiedu.com/api'
项目中所有请求就自动切换到新地址，无需手动替换每一个 URL。 */
/* 设置请求超时时间为 10000 毫秒，也就是 10 秒。

如果请求超过 10 秒还没有响应，就会抛出超时错误。

好处是：避免因为后端死循环或网络卡顿导致页面长时间卡住 */

// 创建 axios 实例
const request = axios.create({
  // baseURL: 'http://localhost:8000/api', // 后端 API 地址
  baseURL: 'https://jsonplaceholder.typicode.com', // 临时使用 JSON 测试接口
  timeout: 10000// 请求超时时间（单位：毫秒）
})

// 请求拦截器（后续可加JWT token）
/* 可以把“钩子函数”想象成：

程序运行过程中预留的“挂钩点”，你可以在这个点“挂上自己的一段逻辑”，系统会在特定时刻自动调用它。

类比现实：

比如你家门口有一个“感应器钩子”——每次有人进门时，它会自动发出提示音。

这个提示音就是你“挂”上去的功能，门感应器就是“钩子”。 */
/* 钩子函数（Hook Function）是框架或库在某个特定事件或生命周期节点中自动调用的函数。

它不是你手动调用的，而是由系统、库或框架“在合适的时机”帮你调用 */
/* 你并没有在代码里手动去调用这个函数。

这个函数会在每次 request.get()、request.post() 发送请求之前被 Axios 自动调用。

你在这里“挂”上一段逻辑，比如加 token，它就会自动在每个请求前运行 */
request.interceptors.request.use(
  config => {
    // 示例：config.headers.Authorization = 'Bearer ' + token
    return config
  },
  error => Promise.reject(error)
)

export default request
