import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import CourseDetails from '../views/CourseDetails.vue'
import ShoppingCart from '../views/ShoppingCart.vue'
import Order from '../views/Order.vue'
import PersonalCenter from '../views/PersonalCenter.vue'
/* 这段代码定义了一个"路由数组"，其中的每一个对象都是一个页面路径与组件的绑定规则。
Vue Router 通过这个配置来控制用户访问不同 URL 时加载哪个页面组件。 */
/* routes：变量名，表示我们要定义的"路由配置数组"。

RouteRecordRaw[]：类型注解，来自 vue-router，表示这个数组中的每一项都是一个合法的"路由对象"。

使用这个类型可以获得 TypeScript 的自动补全与类型检查。 */
/* path: '/'
表示当用户访问根路径（网站首页）时，应该加载哪个组件。

例如：访问 http://localhost:5173/ 就会触发这个路由 */
/* name: 'Home'
给这个路由起了一个名字，叫 'Home'。

这个名称可以用在程序内部进行路由跳转时更直观，比如：

router.push({ name: 'Home' })
而不需要写死路径。 */
/* component: Home
表示这个路径对应要显示的 Vue 组件。

Home 是从文件 ../views/Home.vue 导入进来的一个组件对象。

ts
复制
编辑
import Home from '../views/Home.vue'
当用户访问 /，就会加载并渲染这个 Home.vue 页面。 */
/* 使用 RouteRecordRaw[] 有两个优点：

它是 vue-router 官方提供的类型，可以让 TypeScript 自动提示你哪些字段是合法的（比如 path、component、name 等）。

防止拼写错误或忘写字段导致路由失效 */
//打开网站首页（/），Vue Router 会加载并显示 Home.vue 页面

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login', 
    component: HomeView // 使用HomeView，通过路由控制模态框显示
  },
  {
    path: '/register',
    name: 'Register',
    component: HomeView // 使用HomeView，通过路由控制模态框显示
  },
  {
    path: '/course/:id',
    name: 'CourseDetails',
    component: CourseDetails
  },
  {
    path: '/cart',
    name: 'ShoppingCart',
    component: ShoppingCart
  },
  {
    path: '/order/:id?',
    name: 'Order',
    component: Order
  },
  {
    path: '/user',
    name: 'PersonalCenter',
    component: PersonalCenter
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
