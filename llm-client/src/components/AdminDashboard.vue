<template>
  <div class="admin-dashboard bg-grid-pattern">
    <!-- 顶部导航栏 -->
    <header class="bg-white/90 shadow-sm backdrop-blur-md sticky top-0 z-50">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <i class="fas fa-robot text-purple-600 text-xl"></i>
          <span class="font-bold text-gray-800 text-xl">ModelHub <span class="gradient-text">V1</span></span>
          <span class="hidden md:inline text-sm text-gray-500 ml-2">一站式大语言模型访问平台</span>
        </div>
        <button
            @click="logout"
            class="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-md hover:shadow-lg"
        >
          <i class="fas fa-sign-out-alt mr-1"></i>
          登出
        </button>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="container mx-auto px-4 py-8 flex flex-col items-center justify-center flex-1">
      <div class="admin-card bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl text-center">
        <div class="flex flex-col items-center mb-8">
          <i class="fas fa-user-shield text-purple-600 text-5xl mb-4"></i>
          <h2 class="text-3xl font-bold text-gray-800">管理员仪表板</h2>
          <p class="text-gray-500 mt-2">管理系统核心功能</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <button
              @click="goToFeedback"
              class="function-button bg-gradient-to-r from-blue-500 to-purple-600"
          >
            <i class="fas fa-comment-alt text-2xl mb-2"></i>
            <span>查看反馈信息</span>
          </button>

          <button
              @click="goToUserInformation"
              class="function-button bg-gradient-to-r from-green-500 to-teal-500"
          >
            <i class="fas fa-users text-2xl mb-2"></i>
            <span>查看用户信息</span>
          </button>
        </div>

        <p
            v-if="logoutMessage"
            class="mt-6 text-sm"
            :class="logoutMessage.includes('成功') ? 'text-green-600' : 'text-red-600'"
        >
          {{ logoutMessage }}
        </p>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer bg-white/80 backdrop-blur-md">
      <div class="container mx-auto px-4 py-6">
        <div class="text-center text-sm text-gray-500">
          ©2025 Created by HIT-ModelHub team. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import router from '../router';

export default {
  name: 'AdminDashboard',
  data() {
    return {
      logoutMessage: ''
    };
  },
  methods: {
    logout() {
      router.push({ name: 'Logout' });
    },
    goToFeedback() {
      router.push({ name: 'AdminFeedback' });
    },
    goToUserInformation() {
      router.push({ name: 'AdminUserInfo' });
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.gradient-text {
  background: linear-gradient(90deg, #8b5cf6 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.bg-grid-pattern {
  background-image:
      linear-gradient(to right, rgba(0, 0, 0, 0.03) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(0, 0, 0, 0.03) 1px, transparent 1px);
  background-size: 20px 20px;
}

.admin-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.admin-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.function-button {
  @apply flex flex-col items-center justify-center p-6 rounded-xl text-white font-medium transition-all duration-300;
  @apply hover:shadow-lg hover:opacity-90 transform hover:-translate-y-1;
}

.function-button i {
  @apply text-white;
}

/* 确保Font Awesome图标正常显示 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
</style>