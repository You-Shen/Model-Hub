<template>
  <div>
    <!-- 顶部导航栏 -->
    <header class="bg-white/90 shadow-sm">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <i class="fas fa-robot text-purple-600 text-xl"></i>
          <span class="font-bold text-gray-800">ModelHub V2 <span class="text-purple-600">V2</span></span>
          <span class="hidden md:inline text-sm text-gray-500 ml-2">一站式大语言模型访问平台</span>
        </div>
        <div class="flex items-center space-x-4">
          <a href="#" class="text-gray-600 hover:text-purple-600 transition">帮助中心</a>
          <a href="#" class="text-gray-600 hover:text-purple-600 transition">关于我们</a>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="gradient-bg min-h-screen flex items-center justify-center p-4">
      <div class="retrieve-card rounded-2xl overflow-hidden w-full max-w-md">
        <div class="p-8">
          <!-- 标题 -->
          <div class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">找回密码</h1>
            <p class="text-gray-500">请输入您的邮箱和验证码重置密码</p>
          </div>

          <!-- 找回密码表单 -->
          <form @submit.prevent="retrieve" class="space-y-6">
            <!-- 邮箱输入 -->
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-1">邮箱：</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i class="fas fa-envelope text-gray-400"></i>
                </div>
                <div class="flex">
                  <input
                      type="email"
                      id="email"
                      v-model="email"
                      placeholder="请输入邮箱"
                      class="input-field pl-10 w-full px-4 py-1 rounded-lg border border-gray-300 focus:border-purple-500 focus:outline-none transition"
                      required
                  >
                  <button
                      type="button"
                      :disabled="isSendingCode"
                      @click="sendAuthCode"
                      class="ml-2 px-4 py-1 rounded-lg bg-purple-600 text-white text-sm font-medium hover:bg-purple-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed"
                  >
                    {{ sendButtonText }}
                  </button>
                </div>
              </div>
            </div>

            <!-- 验证码输入 -->
            <div>
              <label for="authcode" class="block text-sm font-medium text-gray-700 mb-1">验证码：</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i class="fas fa-shield-alt text-gray-400"></i>
                </div>
                <input
                    type="text"
                    id="authcode"
                    v-model="authcode"
                    placeholder="请输入验证码"
                    class="input-field pl-10 w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-500 focus:outline-none transition"
                    required
                >
              </div>
            </div>

            <!-- 新密码输入 -->
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-1">新密码：</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i class="fas fa-lock text-gray-400"></i>
                </div>
                <input
                    type="password"
                    id="password"
                    v-model="password"
                    placeholder="请输入新密码"
                    class="input-field pl-10 w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-500 focus:outline-none transition"
                    required
                >
              </div>
            </div>

            <!-- 提交按钮 -->
            <button
                type="submit"
                class="w-full bg-gradient-to-r from-purple-600 to-blue-500 text-white py-3 px-4 rounded-lg font-medium hover:from-purple-700 hover:to-blue-600 transition"
            >
              找回密码
            </button>

            <!-- 消息提示 -->
            <div v-if="message" class="text-center py-2 px-4 rounded-md" :class="message.includes('成功') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
              {{ message }}
            </div>
          </form>

          <!-- 登录链接 -->
          <div class="mt-8 text-center text-sm text-gray-500">
            还记得密码？
            <router-link to="/login" class="text-purple-600 font-medium hover:text-purple-800 transition">点击这里登录</router-link>
          </div>
        </div>

        <!-- 底部装饰 -->
        <div class="bg-gray-50 px-8 py-4 text-center">
          <p class="text-xs text-gray-500">© 2025 ModelHub V2. 保留所有权利。</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

export default {
  name: 'RetrievePassword',
  data() {
    return {
      email: '',
      authcode: '',
      password: '',
      message: '',
      isSendingCode: false,
      countdown: 60,
      timer: null
    };
  },
  computed: {
    sendButtonText() {
      return this.isSendingCode ? `重新发送(${this.countdown}s)` : '发送验证码';
    }
  },
  methods: {
    async sendAuthCode() {
      try {
        this.isSendingCode = true;
        this.countdown = 60;
        this.startCountdown();

        const response = await axios.post('/api/authenticate/retrieve', {
          email: this.email
        });
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response && error.response.data ? error.response.data.message : '验证码发送失败，请稍后重试。';
        this.isSendingCode = false;
        clearInterval(this.timer);
      }
    },
    startCountdown() {
      this.timer = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          this.isSendingCode = false;
          clearInterval(this.timer);
        }
      }, 1000);
    },
    async retrieve() {
      try {
        const response = await axios.post('/api/retrieve', {
          email: this.email,
          authcode: this.authcode,
          password: this.password
        });
        this.message = response.data.message;
        if (response.status === 201) {
          this.message += ' 2s后自动跳转到登录页面...';
          setTimeout(() => {
            this.$router.push('/login');
          }, 2000); // 2秒后重定向到登录页面
        }
      } catch (error) {
        this.message = error.response && error.response.data ? error.response.data.message : '找回密码失败，请稍后重试。';
      }
    }
  }
};
</script>

<style scoped>
.gradient-bg {
  background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
}
.retrieve-card {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.85);
}
.input-field:focus {
  box-shadow: 0 0 0 3px rgba(167, 119, 227, 0.3);
}

/* 确保Font Awesome图标正常显示 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
</style>