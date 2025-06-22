<template>
  <div class="admin-user-page bg-grid-pattern">
    <!-- 顶部导航栏 -->
    <header class="bg-white/90 shadow-sm backdrop-blur-md sticky top-0 z-50">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <i class="fas fa-robot text-purple-600 text-xl"></i>
          <span class="font-bold text-gray-800 text-xl">ModelHub <span class="gradient-text">V2</span></span>
          <span class="hidden md:inline text-sm text-gray-500 ml-2">一站式大语言模型访问平台</span>
        </div>
        <button
            @click="goBack"
            class="px-4 py-2 rounded-lg border-2 border-purple-600 text-purple-600 font-medium hover:bg-purple-50 transition-all duration-300"
        >
          返回仪表板
        </button>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="container mx-auto px-4 py-4">
      <div class="admin-content bg-white rounded-2xl shadow-xl p-6" style="max-height: calc(100vh - 160px);">
        <div class="flex flex-col items-center mb-4">
          <i class="fas fa-users text-purple-600 text-3xl mb-2"></i>
          <h2 class="text-2xl font-bold text-gray-800">用户信息管理</h2>
          <p class="text-gray-500 text-sm">查看和管理系统用户</p>
        </div>

        <div v-if="users.length > 0" class="user-list space-y-3">
          <div
              v-for="user in users"
              :key="user.id"
              class="user-card p-4 rounded-lg border border-gray-200 hover:shadow-md transition-all duration-200"
          >
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p class="text-xs text-gray-500">用户编号</p>
                <p class="font-medium">{{ user.id }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">用户名</p>
                <p class="font-medium">{{ user.username }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">管理员权限</p>
                <p class="font-medium" :class="user.is_admin ? 'text-green-600' : 'text-gray-600'">
                  {{ user.is_admin ? '是' : '否' }}
                  <i v-if="user.is_admin" class="fas fa-shield-alt ml-1"></i>
                </p>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-8">
          <i class="fas fa-user-slash text-gray-300 text-4xl mb-3"></i>
          <p class="text-gray-500 text-sm">暂无用户信息</p>
        </div>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer bg-white/80 backdrop-blur-md">
      <div class="container mx-auto px-4 py-4">
        <div class="text-center text-xs text-gray-500">
          ©2025 Created by HIT-ModelHub team. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';
import router from "@/router";
axios.defaults.withCredentials = true;

export default {
  name: 'UserInformation',
  data() {
    return {
      users: []
    };
  },
  async created() {
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('/api/admin/users', { withCredentials: true });
        this.users = response.data.users;
      } catch (error) {
        console.error('获取用户信息失败：', error);
      }
    },
    goBack() {
      router.push({ name: 'AdminDashboard' });
    }
  }
};
</script>

<style scoped>
.admin-user-page {
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

.admin-content {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.user-list {
  max-height: calc(100vh - 300px);
  overflow-y: auto;
  padding-right: 8px;
}

/* 自定义滚动条 */
.user-list::-webkit-scrollbar {
  width: 6px;
}

.user-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.user-list::-webkit-scrollbar-thumb {
  background: #c4c4c4;
  border-radius: 10px;
}

.user-list::-webkit-scrollbar-thumb:hover {
  background: #a0a0a0;
}

/* 确保Font Awesome图标正常显示 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
</style>