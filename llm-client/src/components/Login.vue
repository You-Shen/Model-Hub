<template>
  <div>
    <!-- 顶部导航栏 -->
    <header class="bg-white/90 shadow-sm">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <i class="fas fa-robot text-purple-600 text-xl"></i>
          <span class="font-bold text-gray-800">ModelHub <span class="text-purple-600">V2</span></span>
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
      <div class="login-card rounded-2xl overflow-hidden w-full max-w-md">
        <div class="p-8">
          <!-- 欢迎标题 -->
          <div class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">欢迎回来!</h1>
            <p class="text-gray-500">请登录您的账户继续使用AI服务</p>
          </div>

          <!-- 登录表单 -->
          <form @submit.prevent="login" class="space-y-6">
            <!-- 用户名输入 -->
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700 mb-1">用户名/邮箱：</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i class="fas fa-user text-gray-400"></i>
                </div>
                <input
                    type="text"
                    id="username"
                    v-model="username"
                    placeholder="请输入用户名或邮箱"
                    class="input-field pl-10 w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-500 focus:outline-none transition"
                    required
                >
              </div>
            </div>

            <!-- 密码输入 -->
            <div>
              <div class="flex justify-between items-center mb-1">
                <label for="password" class="block text-sm font-medium text-gray-700">密码：</label>
                <!--                <a href="#" class="text-sm text-purple-600 hover:text-purple-800 transition">忘记密码?</a>-->
                <router-link to="/retrieve-password" class="text-purple-600 font-medium text-sm hover:text-purple-600 transition">忘记密码？</router-link>
              </div>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i class="fas fa-lock text-gray-400"></i>
                </div>
                <input
                    type="password"
                    id="password"
                    v-model="password"
                    placeholder="请输入密码"
                    class="input-field pl-10 w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-500 focus:outline-none transition"
                    required
                >
              </div>
            </div>

            <!-- 登录按钮 -->
            <button
                type="submit"
                class="login-btn w-full bg-gradient-to-r from-purple-600 to-blue-500 text-white py-3 px-4 rounded-lg font-medium hover:from-purple-700 hover:to-blue-600 transition"
            >
              登录
            </button>

            <!-- 错误消息 -->
            <div v-if="message" class="text-center py-2 px-4 rounded-md bg-red-100 text-red-700">
              {{ message }}
            </div>
          </form>

          <!-- 注册链接 -->
          <div class="mt-8 text-center text-sm text-gray-500">
            还没有账号?
            <router-link to="/register" class="text-purple-600 font-medium hover:text-purple-800 transition">立即注册</router-link>
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
import router from '@/router/index.js';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/login', {
          username: this.username,
          password: this.password
        }, { withCredentials: true });
        this.message = response.data.message;
        if (response.data.role === 'admin') {
          router.push({ name: 'AdminDashboard' });
        } else {
          router.push({ name: 'UserDashboard' });
        }
      } catch (error) {
        this.message = error.response && error.response.data ? error.response.data.message : '登录失败，请稍后重试。';
      }
    }
  }
};
</script>

<style scoped>
.gradient-bg {
  background: linear-gradient(135deg, #6e8efb 0%, #a777e3 100%);
}
.login-card {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.85);
}
.input-field:focus {
  box-shadow: 0 0 0 3px rgba(167, 119, 227, 0.3);
}
.login-btn {
  transition: all 0.3s ease;
}
.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

/* 确保Font Awesome图标正常显示 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
</style>