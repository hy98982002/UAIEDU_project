<!-- 登录模态框组件 - 基于原始设计，支持多种登录方式 -->
<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="login-container-wrapper" @click.stop>
      <!-- 主登录容器 -->
      <div class="login-container">
        <!-- 关闭按钮 -->
        <span class="close-btn" @click="closeModal">
          <i>×</i>
        </span>

        <!-- 密码登录表单 -->
        <div v-show="loginType === 'password'" id="password-login">
          <h4 class="text-center mt-4">密码登录</h4>
          <form class="mt-5" @submit.prevent="handlePasswordLogin">
            <div class="mb-3">
              <div class="input-group">
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="passwordForm.phoneNumber"
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
            <button type="submit" class="btn btn-dark w-100 mt-4">登录</button>

            <!-- 其他登录方式 -->
            <div class="other-login-methods">
              其他登陆方式
            </div>
            <div class="login-icons">
              <div class="login-icon" @click.stop="switchToWechatLogin">
                <i class="fab fa-weixin wechat-icon"></i>
              </div>
              <div class="login-icon" @click.stop="switchToCodeLogin">
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
        <div v-show="loginType === 'code'" id="code-login">
          <h4 class="text-center mt-4">手机验证码登录</h4>
          <form class="mt-5" @submit.prevent="handleCodeLogin">
            <div class="mb-3">
              <div class="input-group">
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="codeForm.phoneNumber"
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
                  @click="sendVerificationCode"
                  :disabled="countdown > 0"
                >
                  {{ countdown > 0 ? `${countdown}秒后重新获取` : '获取验证码' }}
                </button>
              </div>
            </div>
            <button type="submit" class="btn btn-dark w-100 mt-4">登录</button>

            <!-- 其他登录方式 -->
            <div class="other-login-methods">
              其他登陆方式
            </div>
            <div class="login-icons">
              <div class="login-icon" @click.stop="switchToWechatLogin">
                <i class="fab fa-weixin wechat-icon"></i>
              </div>
              <div class="login-icon" @click.stop="switchToPasswordLogin">
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
        <div v-show="loginType === 'wechat'" id="wechat-login">
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
            <div class="login-icon" @click.stop="switchToPasswordLogin">
              <i class="fas fa-key key-icon"></i>
            </div>
            <div class="login-icon" @click.stop="switchToCodeLogin">
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
      </div>

      <!-- 底部黄色区域 -->
      <div class="yellow-footer">
        <div class="text-center mt-4" style="font-size: 17px">
          <p>
            我还没有账户 
            <a href="#" class="text-primary" @click="goToRegister">去注册</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

// Props和Emits
const emit = defineEmits(['close'])
const router = useRouter()

// 当前登录类型
const loginType = ref('password') // 'password', 'code', 'wechat'

// 倒计时状态
const countdown = ref(0)
let countdownTimer = null

// 表单数据
const passwordForm = ref({
  phoneNumber: '',
  password: '',
  agreement: false
})

const codeForm = ref({
  phoneNumber: '',
  verificationCode: '',
  agreement: false
})

const wechatForm = ref({
  agreement: false
})

// 组件挂载
onMounted(() => {
  // 组件挂载时的初始化逻辑
})

// 清理定时器
onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})

// 切换登录方式
const switchToPasswordLogin = () => {
  loginType.value = 'password'
}

const switchToCodeLogin = () => {
  loginType.value = 'code'
}

const switchToWechatLogin = () => {
  loginType.value = 'wechat'
}

// 发送验证码
const sendVerificationCode = () => {
  const phoneNumber = codeForm.value.phoneNumber

  if (!phoneNumber) {
    alert('请先输入手机号')
    return
  }

  // 手机号格式验证
  const phoneRegex = /^1[3-9]\d{9}$/
  if (!phoneRegex.test(phoneNumber)) {
    alert('请输入正确的手机号码')
    return
  }

  // 开始倒计时
  startCountdown()
  
  // TODO: 调用后端API发送验证码
  console.log(`向 ${phoneNumber} 发送验证码`)
  alert('验证码已发送')
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

// 表单提交方法
const handlePasswordLogin = () => {
  if (!passwordForm.value.phoneNumber || !passwordForm.value.password) {
    alert('请填写完整的登录信息')
    return
  }
  
  if (!passwordForm.value.agreement) {
    alert('请同意用户协议')
    return
  }
  
  // TODO: 调用后端API进行登录
  console.log('密码登录:', passwordForm.value)
  alert('登录功能待实现')
  closeModal()
}

const handleCodeLogin = () => {
  if (!codeForm.value.phoneNumber || !codeForm.value.verificationCode) {
    alert('请填写完整的登录信息')
    return
  }
  
  if (!codeForm.value.agreement) {
    alert('请同意用户协议')
    return
  }
  
  // TODO: 调用后端API进行登录
  console.log('验证码登录:', codeForm.value)
  alert('登录功能待实现')
  closeModal()
}

// 关闭模态框
const closeModal = () => {
  emit('close')
}

const handleOverlayClick = () => {
  closeModal()
}

// 跳转到注册
const goToRegister = () => {
  closeModal()
  router.push('/register')
}
</script>

<style scoped>
/* 模态框遮罩层 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease-out;
}

/* 登录容器包装器 */
.login-container-wrapper {
  animation: slideUp 0.3s ease-out;
}

/* 主登录容器 */
.login-container {
  max-width: 430px;
  background-color: #FBFBF6;
  padding: 20px 30px;
  border-radius: 15px;
  margin: auto;
  position: relative;
  z-index: 2;
}

/* 关闭按钮 */
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
}

.close-btn i {
  margin-top: -4px;
  display: block;
  line-height: 1;
}

/* 表单控件 */
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

/* 登录按钮 */
.btn-dark {
  background-color: black;
  color: white;
  border-radius: 15px;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  transition: none;
  height: 50px;
}

.btn-dark:hover {
  background-color: #2c2c2c;
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
}

.verification-code-btn:hover,
.verification-code-btn:focus {
  color: #0056b3;
  text-decoration: none;
  outline: none;
}

.verification-code-btn:disabled {
  color: #6c757d;
  cursor: not-allowed;
}

/* 输入框容器相对定位 */
.code-input-container {
  position: relative;
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

/* 图标颜色 */
.wechat-icon {
  color: #07C160;
}

.phone-icon {
  color: #6c757d;
}

.key-icon {
  color: #888888;
}

/* 微信登录二维码容器 */
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

/* 用户协议样式 */
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

.text-link {
  color: #007bff;
  text-decoration: none;
}

.text-link:hover {
  color: #007bff;
  text-decoration: underline;
}

/* 底部黄色区域 */
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
}

.yellow-footer a:hover {
  text-decoration: underline;
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-container {
    padding: 15px 20px;
    margin: 1rem;
    max-width: 90%;
  }
  
  .yellow-footer {
    max-width: 90%;
    margin: 1rem auto;
    margin-top: -12px;
  }
}
</style> 