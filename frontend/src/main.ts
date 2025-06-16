import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './store'

import '@coreui/coreui/dist/css/coreui.min.css'   // CoreUI 样式

// 引入 Bootstrap 样式
import 'bootstrap/dist/css/bootstrap.min.css'

const app = createApp(App)
app.use(router)
app.use(pinia)// 绑定全局 pinia 实例
app.mount('#app')
