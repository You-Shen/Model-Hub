<template>
  <div class="admin-dashboard bg-grid-pattern">
    <!-- 顶部导航栏 -->
    <header class="bg-white/90 shadow-sm backdrop-blur-md sticky top-0 z-50">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <i class="fas fa-robot text-purple-600 text-xl"></i>
          <span class="font-bold text-gray-800 text-xl">ChatWithAIs <span class="gradient-text">V2</span></span>
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
      <div class="admin-card bg-white rounded-2xl shadow-xl p-8 w-full max-w-4xl text-center">
        <div class="flex flex-col items-center mb-8">
          <i class="fas fa-user-shield text-purple-600 text-5xl mb-4"></i>
          <h2 class="text-3xl font-bold text-gray-800">管理员仪表板</h2>
          <p class="text-gray-500 mt-2">管理系统核心数据统计</p>
        </div>

        <!-- 统计信息卡片 -->
        <div class="stats-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <!-- 总人数 -->
          <div class="stat-card bg-gradient-to-br from-blue-50 to-purple-50 p-6 rounded-xl">
            <div class="text-3xl font-bold text-purple-600 mb-2">{{ value2 || '--' }}</div>
            <div class="text-gray-600">{{ title2 }}</div>
            <button @click="goToUserInformation" class="mt-3 text-purple-600 hover:text-purple-800 transition">
              <i class="fas fa-eye mr-1"></i>查看详情
            </button>
          </div>

          <!-- 增长人数 -->
          <div class="stat-card bg-gradient-to-br from-green-50 to-teal-50 p-6 rounded-xl">
            <div class="text-3xl font-bold text-teal-600 mb-2">{{ value1 || '--' }}</div>
            <div class="text-gray-600">{{ title1 }}</div>
            <button @click="goToCreaseUserInfo" class="mt-3 text-teal-600 hover:text-teal-800 transition">
              <i class="fas fa-chart-line mr-1"></i>查看趋势
            </button>
          </div>

          <!-- 未读反馈 -->
          <div class="stat-card bg-gradient-to-br from-amber-50 to-orange-50 p-6 rounded-xl">
            <div class="text-3xl font-bold text-orange-600 mb-2">{{ unread_feedback || '--' }}</div>
            <div class="text-gray-600">未读反馈</div>
            <button @click="goToUnreadFeedback" class="mt-3 text-orange-600 hover:text-orange-800 transition">
              <i class="fas fa-inbox mr-1"></i>处理反馈
            </button>
          </div>

          <!-- 总反馈数 -->
          <div class="stat-card bg-gradient-to-br from-red-50 to-pink-50 p-6 rounded-xl">
            <div class="text-3xl font-bold text-pink-600 mb-2">{{ value3 || '--' }}</div>
            <div class="text-gray-600">{{ title3 }}</div>
            <button @click="goToFeedback" class="mt-3 text-pink-600 hover:text-pink-800 transition">
              <i class="fas fa-comments mr-1"></i>查看全部
            </button>
          </div>
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
import axios from 'axios';
import router from "@/router";

export default {
  name: 'AdminDashboard',
  data() {
    return {
      like: true,
      value1: null,
      value2: null,
      value3: null,
      title1: "增长人数(较上月的今天)",
      title2: "总人数",
      title3: "总反馈数",
      unread_feedback:null,
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
    },
    goToCreaseUserInfo() {
      router.push({ name: 'UserCreaseInfo' });
    },
    goToUnreadFeedback() {
      router.push({ name: 'AdminUnreadFeedback' });
    },
    // 获取总人数
    fetchUserCount() {
      axios.get('/api/admin/number_user', { withCredentials: true })
          .then(response => {
            this.value2 = response.data.total_users;
          })
          .catch(error => {
            console.error("There was an error fetching the user count:", error);
          });
    },
    // 获取增长人数
    fetchIncreaseUserCount() {
      axios.get('/api/admin/increase_user', { withCredentials: true })
          .then(response => {
            this.value1 = response.data.increase_users;
          })
          .catch(error => {
            console.error("There was an error fetching the increase user count:", error);
          });
    },
    // 获取未读反馈数量
    fetchUnreadFeedbackCount() {
      axios.get('/api/admin/number_unreadfeedback', { withCredentials: true })
          .then(response => {
            this.unread_feedback = response.data.unread_feedback;
          })
          .catch(error => {
            console.error("There was an error fetching the unread feedback count:", error);
          });
    },
    // 获取未读反馈数量
    fetchAllFeedbackCount() {
      axios.get('/api/admin/number_allfeedback', { withCredentials: true })
          .then(response => {
            this.value3 = response.data.allfeedback;
          })
          .catch(error => {
            console.error("There was an error fetching the all feedback count:", error);
          });
    },
  },

  // 钩子 处于该界面自动获取
  created() {
    this.fetchUserCount();
    this.fetchIncreaseUserCount();
    this.fetchUnreadFeedbackCount();
    this.fetchAllFeedbackCount();
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

.stat-card {
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.stats-grid {
  perspective: 1000px;
}

/* 确保Font Awesome图标正常显示 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
</style>