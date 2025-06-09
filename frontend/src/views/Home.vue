<template>
  <div class="container mt-5">
    <h1 class="text-primary">UAI 教育平台首页</h1>
    <p>欢迎使用 Vite + Vue3 + Bootstrap + Pinia 构建的前端架构</p>

    <hr />

    <h3>📦 模拟文章列表（axios 请求演示）</h3>
    <ul class="list-group">
      <li class="list-group-item" v-for="post in posts" :key="post.id">
        {{ post.title }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">//表示这个 <script> 使用了 Vue 3 的 Composition API 的语法糖模式，
// 并且启用了 TypeScript 类型支持（lang="ts"）

/* 从 vue 中导入两个组合式 API：

ref：用于声明响应式变量（替代 data() 中的变量）

onMounted：生命周期钩子，组件挂载后自动执行某段逻辑（如发起网络请求） */
import { ref, onMounted } from 'vue'
import { fetchPosts } from '../api/posts'

/* 使用 ref 定义一个响应式的数组变量 posts，类型是 any[]，初始值为空数组。

它会绑定在模板 <template> 中，通过 v-for 动态渲染。

TypeScript 使用 ref<any[]>([]) 是为了让 IDE 正确识别它是“数组型响应式变量”。 */
const posts = ref<any[]>([])
  /* 注册一个生命周期钩子函数 onMounted，它会在组件第一次挂载（进入 DOM）之后立即执行。

这非常适合放置初始化加载数据的逻辑（比如加载课程、文章、用户信息等） */
/* 调用之前引入的接口函数 fetchPosts()，并使用 await 等待返回结果。

返回的是一个 axios 响应对象（包含 data、status 等字段） */
/* 把接口返回的文章列表（res.data）赋值给响应式变量 posts。

⚠️ 注意：因为 ref 创建的变量需要通过 .value 访问其实际值（这是 Vue 3 的响应式代理机制）。

一旦赋值，页面绑定了这个变量的部分会自动更新 DOM 渲染（你使用了 v-for="post in posts" */

onMounted(async () => {
  const res = await fetchPosts()
  posts.value = res.data
})//异步函数结束，生命周期函数注册完毕
/* 在页面加载时自动通过 axios 调用接口 /posts 获取文章列表，并将数据存入 posts 变量，供模板动态渲染使用。 */
</script>
