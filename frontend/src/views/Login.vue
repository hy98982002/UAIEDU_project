<template>
  <div style="background-color: black; min-height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
    <!-- 登录容器 -->
    <div class="login-container">
      <!-- 关闭按钮 -->
      <span class="close-btn" @click="closeDialog">
        <i>×</i>
      </span>

      <!-- 密码登录表单 -->
      <div v-if="currentForm === 'password'" class="form-section">
        <h4 class="text-center mt-4">密码登录</h4>
        <form class="mt-5" @submit.prevent="handlePasswordLogin">
          <div class="mb-3">
            <div class="input-group">
              <input 
                type="text" 
                class="form-control" 
                v-model="passwordForm.phone"
                placeholder="请输入手机号"
                required
              >
            </div>
          </div>
          <div class="mb-3 mt-4">
            <input 
              type="password" 
              class="form-control" 
              v-model="passwordForm.password"
              placeholder="请输入登录密码"
              required
            >
          </div>
          <button type="submit" class="btn btn-dark w-100 mt-4" :disabled="!isPasswordFormValid">
            登录
          </button>

          <!-- 其他登录方式 -->
          <div class="other-login-methods">
            其他登陆方式
          </div>
          <div class="login-icons">
            <div class="login-icon" @click="switchForm('wechat')">
              <i class="fab fa-weixin wechat-icon"></i>
            </div>
            <div class="login-icon" @click="switchForm('code')">
              <i class="fas fa-mobile-alt phone-icon"></i>
            </div>
          </div>

          <!-- 用户协议复选框 -->
          <div class="form-check mt-4 text-center">
            <input 
              class="form-check-input" 
              type="checkbox" 
              v-model="passwordForm.agreement"
              id="agreement"
              required
            >
            <label class="form-check-label" for="agreement">
              我已阅读并同意 <a href="#" class="text-link">《用户协议与服务条款》</a>
            </label>
          </div>
        </form>
      </div>

      <!-- 手机验证码登录表单 -->
      <div v-if="currentForm === 'code'" class="form-section">
        <h4 class="text-center mt-4">手机验证码登录</h4>
        <form class="mt-5" @submit.prevent="handleCodeLogin">
          <div class="mb-3">
            <div class="input-group">
              <input 
                type="text" 
                class="form-control" 
                v-model="codeForm.phone"
                placeholder="请输入手机号"
                required
              >
            </div>
          </div>
          <div class="mb-3 mt-4">
            <div class="code-input-container">
              <input 
                type="text" 
                class="form-control" 
                v-model="codeForm.verificationCode"
                placeholder="请输入验证码"
                required
              >
              <button 
                class="verification-code-btn" 
                type="button"
                @click="sendVerificationCode('code')"
                :disabled="countdown > 0"
              >
                {{ countdown > 0 ? `${countdown}秒后重新获取` : '获取验证码' }}
              </button>
            </div>
          </div>
          <button type="submit" class="btn btn-dark w-100 mt-4" :disabled="!isCodeFormValid">
            登录
          </button>

          <!-- 其他登录方式 -->
          <div class="other-login-methods">
            其他登陆方式
          </div>
          <div class="login-icons">
            <div class="login-icon" @click="switchForm('wechat')">
              <i class="fab fa-weixin wechat-icon"></i>
            </div>
            <div class="login-icon" @click="switchForm('password')">
              <i class="fas fa-key key-icon"></i>
            </div>
          </div>

          <!-- 用户协议复选框 -->
          <div class="form-check mt-4 text-center">
            <input 
              class="form-check-input" 
              type="checkbox" 
              v-model="codeForm.agreement"
              id="agreementCode"
              required
            >
            <label class="form-check-label" for="agreementCode">
              我已阅读并同意 <a href="#" class="text-link">《用户协议与服务条款》</a>
            </label>
          </div>
        </form>
      </div>

      <!-- 微信登录表单 -->
      <div v-if="currentForm === 'wechat'" class="form-section">
        <h4 class="text-center mt-4">微信登录</h4>
        <div class="qr-code-container">
          <i class="fab fa-weixin fa-5x wechat-icon"></i>
        </div>
        <p class="text-center">请使用微信扫描二维码登录</p>

        <!-- 其他登录方式 -->
        <div class="other-login-methods">
          其他登陆方式
        </div>
        <div class="login-icons">
          <div class="login-icon" @click="switchForm('password')">
            <i class="fas fa-key key-icon"></i>
          </div>
          <div class="login-icon" @click="switchForm('code')">
            <i class="fas fa-mobile-alt phone-icon"></i>
          </div>
        </div>

        <!-- 用户协议复选框 -->
        <div class="form-check mt-4 text-center">
          <input 
            class="form-check-input" 
            type="checkbox" 
            v-model="wechatForm.agreement"
            id="agreementWechat"
            required
          >
          <label class="form-check-label" for="agreementWechat">
            我已阅读并同意 <a href="#" class="text-link">《用户协议与服务条款》</a>
          </label>
        </div>
      </div>

      <!-- 注册表单 -->
      <div v-if="currentForm === 'register'" class="form-section">
        <h4 class="text-center mt-4">输入手机号及验证码</h4>
        <form class="mt-5" @submit.prevent="handleRegisterSubmit">
          <div class="mb-3">
            <div class="input-group">
              <input 
                type="text" 
                class="form-control" 
                v-model="registerForm.phone"
                placeholder="请输入手机号"
                required
              >
            </div>
          </div>
          <div class="mb-3 mt-4">
            <div class="code-input-container">
              <input 
                type="text" 
                class="form-control" 
                v-model="registerForm.verificationCode"
                placeholder="请输入验证码"
                required
              >
              <button 
                class="verification-code-btn" 
                type="button"
                @click="sendVerificationCode('register')"
                :disabled="countdown > 0"
              >
                {{ countdown > 0 ? `${countdown}秒后重新获取` : '获取验证码' }}
              </button>
            </div>
          </div>
          <button type="submit" class="btn btn-dark w-100 mt-4" :disabled="!isRegisterFormValid">
            提交注册
          </button>

          <!-- 用户协议复选框 -->
          <div class="form-check text-center" id="form-check">
            <input 
              class="form-check-input" 
              type="checkbox" 
              v-model="registerForm.agreement"
              id="agreementRegister"
              required
            >
            <label class="form-check-label" for="agreementRegister">
              我已阅读并同意 <a href="#" class="text-link">《用户协议与服务条款》</a>
            </label>
          </div>
        </form>
      </div>
    </div>

    <!-- 底部黄色区域 -->
    <div class="yellow-footer">
      <div class="text-center mt-4" style="font-size: 17px">
        <p>
          <span v-if="currentForm === 'register'">
            已有账户 <a href="#" class="text-primary" @click.prevent="switchForm('password')">去登录</a>
          </span>
          <span v-else>
            我还没有账户 <a href="#" class="text-primary" @click.prevent="switchForm('register')">去注册</a>
          </span>
        </p>
      </div>
    </div>

    <!-- 提示消息 -->
    <div v-if="message" class="alert alert-info mt-3" style="position: fixed; top: 20px; right: 20px; z-index: 9999;">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import { AuthService } from '@/services/auth'
import api from '@/utils/axios'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 当前显示的表单类型
const currentForm = ref('password') // 'password' | 'code' | 'wechat' | 'register'

// 倒计时状态
const countdown = ref(0)
let countdownTimer = null

// 提示消息
const message = ref('')

// 各个表单的数据
const passwordForm = ref({
  phone: '',
  password: '',
  agreement: false
})

const codeForm = ref({
  phone: '',
  verificationCode: '',
  agreement: false
})

const wechatForm = ref({
  agreement: false
})

const registerForm = ref({
  phone: '',
  verificationCode: '',
  agreement: false
})

// 表单验证计算属性
const isPasswordFormValid = computed(() => {
  return passwordForm.value.phone &&
         passwordForm.value.password &&
         passwordForm.value.agreement
})

const isCodeFormValid = computed(() => {
  return codeForm.value.phone &&
         codeForm.value.verificationCode &&
         codeForm.value.agreement
})

const isRegisterFormValid = computed(() => {
  return registerForm.value.phone &&
         registerForm.value.verificationCode &&
         registerForm.value.agreement
})

// 表单切换方法
const switchForm = (formType) => {
  currentForm.value = formType
}

// 发送验证码
const sendVerificationCode = async (formType) => {
  let phone = ''
  
  if (formType === 'code') {
    phone = codeForm.value.phone
  } else if (formType === 'register') {
    phone = registerForm.value.phone
  }

  if (!phone) {
    showMessage('请先输入手机号')
    return
  }

  // 手机号格式验证
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(phone)) {
    showMessage('请输入正确的手机号码')
    return
  }

  try {
    // 开始倒计时
    startCountdown()
    
    // 调用AuthService发送验证码
    await AuthService.sendSmsCode(phone)
    showMessage('验证码已发送')
  } catch (error) {
    // 发送失败时停止倒计时
    if (countdownTimer) {
      clearInterval(countdownTimer)
      countdown.value = 0
    }
    showMessage(error.message || '验证码发送失败，请重试')
  }
}

// 倒计时功能
const startCountdown = () => {
  countdown.value = 60
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer)
      countdownTimer = null
    }
  }, 1000)
}

// 显示提示消息
const showMessage = (msg) => {
  message.value = msg
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

// 表单提交方法
const handlePasswordLogin = async () => {
  try {
    const success = await authStore.login(passwordForm.value.phone, passwordForm.value.password)
    if (success) {
      showMessage('登录成功！')
      // 跳转到redirect指定的页面或首页
      const redirect = route.query.redirect || '/'
      router.push(redirect)
    }
  } catch (error) {
    showMessage(error.message || '登录失败，请重试')
  }
}

const handleCodeLogin = async () => {
  try {
    // 使用AuthService进行短信验证码登录
    const { access, refresh, user } = await AuthService.smsLogin(
      codeForm.value.phone, 
      codeForm.value.verificationCode
    )
    
    authStore.setTokens(access, refresh)
    authStore.setUserInfo(user)
    
    showMessage('登录成功！')
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (error) {
    showMessage(error.message || '验证码登录失败，请重试')
  }
}

const handleRegisterSubmit = () => {
  console.log('注册表单提交:', registerForm.value)
  showMessage('注册信息提交成功！')
  
  // TODO: 调用后端API提交注册信息
  // 注册成功后可以跳转到完善信息页面或直接登录
}

// 关闭对话框
const closeDialog = () => {
  console.log('关闭对话框')
  // 可以发射事件或者路由跳转
  // router.go(-1) // 返回上一页
}

// 组件销毁时清理计时器
onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>

<style scoped>
.login-container {
  max-width: 430px;
  background-color: #FBFBF6;
  padding: 20px 30px;
  border-radius: 15px;
  margin: auto;
  position: relative;
  z-index: 2;
}

.toggle-btn {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: white;
  color: black;
  border: 1px solid #ddd;
  border-radius: 15px;
  text-align: center;
  cursor: pointer;
  margin-top: 15px;
  -webkit-text-stroke: 0.1px black;
  transition: background-color 0.3s ease;
}

.toggle-btn:hover {
  background-color: #e0e0e0;
}

.btn-dark {
  background-color: black;
  color: white;
  border-radius: 15px;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  transition: background-color 0.3s ease;
  height: 50px;
}

.btn-dark:hover:not(:disabled) {
  background-color: #2c2c2c;
}

.btn-dark:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.form-control {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  height: 50px;
  transition: border-color 0.3s ease;
}

.form-control:hover,
.form-control:focus,
.form-control:active,
.form-control:focus-visible {
  border-color: black;
  box-shadow: none !important;
  outline: none !important;
}

/* 验证码按钮样式 */
.verification-code-btn {
  background-color: #f2f2f2;
  color: #007bff;
  font-weight: 500;
  font-size: 14px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  padding: 7px 14px;
  margin-right: 10px;
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  transition: all 0.3s ease;
}

.verification-code-btn:hover:not(:disabled),
.verification-code-btn:focus:not(:disabled) {
  color: #0056b3;
  background-color: #e9ecef;
  text-decoration: none;
  outline: none;
}

.verification-code-btn:disabled {
  background-color: #e9ecef;
  color: #6c757d;
  cursor: not-allowed;
}

.code-input-container {
  position: relative;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 50%;
  width: 25px;
  height: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.close-btn i {
  margin-top: -4px;
  display: block;
  line-height: 1;
}

.text-link {
  color: #007bff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.text-link:hover {
  color: #0056b3;
  text-decoration: none;
}

.form-check {
  font-size: 13px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.form-check-input {
  margin-top: 0.35em;
  float: none;
}

.form-check-label {
  margin-left: 0.25rem;
}

.yellow-footer {
  margin: auto;
  max-width: 430px;
  height: 80px;
  background-color: #f8cc61;
  padding: 10px 20px;
  text-align: center;
  color: black;
  font-size: 16px;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
  position: relative;
  z-index: 1;
  margin-top: -12px;
}

.yellow-footer a {
  color: #007bff;
  text-decoration: none;
  transition: color 0.3s ease;
}

.yellow-footer a:hover {
  color: #0056b3;
  text-decoration: underline;
}

.text-center {
  margin-top: 70px;
}

#form-check {
  margin-top: 25px;
  margin-bottom: 30px;
}

/* 其他登录方式样式 */
.other-login-methods {
  text-align: center;
  margin-top: 20px;
  position: relative;
}

.other-login-methods::before,
.other-login-methods::after {
  content: "";
  display: inline-block;
  width: 30%;
  height: 1px;
  background-color: #ddd;
  vertical-align: middle;
  margin: 0 10px;
}

.login-icons {
  display: flex;
  justify-content: center;
  margin-top: 15px;
  gap: 40px;
}

.login-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-icon:hover {
  background-color: #e0e0e0;
}

.login-icon i {
  font-size: 20px;
}

/* 微信图标颜色 */
.wechat-icon {
  color: #07C160;
}

/* 手机图标颜色 */
.phone-icon {
  color: #6c757d;
}

/* 钥匙图标颜色 */
.key-icon {
  color: #888888;
}

/* 微信登录表单 */
.qr-code-container {
  margin: 20px auto;
  width: 180px;
  height: 180px;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

/* 表单动画 */
.form-section {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    margin: 20px;
    padding: 15px 20px;
  }
  
  .yellow-footer {
    margin: 20px;
    margin-top: -12px;
  }
  
  .login-icons {
    gap: 30px;
  }
}
</style> 