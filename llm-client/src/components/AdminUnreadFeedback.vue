<template>
  <div class="admin-feedback-page bg-grid-pattern">
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
          返回
        </button>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="container mx-auto px-4 py-4">
      <div class="admin-content bg-white rounded-2xl shadow-xl p-6" style="max-height: calc(100vh - 160px);">
        <div class="flex flex-col items-center mb-4">
          <i class="fas fa-comment-alt text-purple-600 text-3xl mb-2"></i>
          <h2 class="text-2xl font-bold text-gray-800">未读反馈信息</h2>
        </div>

        <div v-if="feedbacks.length > 0" class="feedback-list flex-grow space-y-auto" style="max-height: calc(100vh - 300px); overflow-y: auto;">
          <div
              v-for="feedback in feedbacks"
              :key="feedback.id"
              class="feedback-card p-4 mb-3 rounded-lg border border-gray-200 hover:shadow-md transition-all duration-200 last:mb-0"
          >
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <p class="text-xs text-gray-500">反馈编号</p>
                <p class="font-medium text-sm">{{ feedback.id }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">用户编号</p>
                <p class="font-medium text-sm">{{ feedback.user_id }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">用户名</p>
                <p class="font-medium text-sm">{{ feedback.username }}</p>
              </div>
              <div>
                <p class="text-xs text-gray-500">提交时间</p>
                <p class="font-medium text-sm">{{ new Date(feedback.timestamp).toLocaleString() }}</p>
              </div>
            </div>
            <div class="mt-3">
              <p class="text-xs text-gray-500">反馈内容</p>
              <p class="mt-1 p-2 bg-gray-50 rounded text-sm">{{ feedback.message }}</p>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-8">
          <i class="fas fa-inbox text-gray-300 text-4xl mb-3"></i>
          <p class="text-gray-500 text-sm">暂无未读反馈</p>
        </div>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer bg-white/80 backdrop-blur-md mt-auto">
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

export default {
  name: 'AdminFeedback',
  data() {
    return {
      feedbacks: []
    };
  },
  async created() {
    await this.fetchFeedbacks();
  },
  methods: {
    async fetchFeedbacks() {
      try {
        const response = await axios.get('/api/admin/unreadfeedback', { withCredentials: true });
        this.feedbacks = response.data.feedbacks;
      } catch (error) {
        console.error('获取反馈信息时出错：', error);
      }
    },
    goBack() {
      // 返回到之前的对话页面的逻辑
      router.push({ name: 'AdminDashboard' });
    }
  }
};
</script>

<style scoped>
.admin-feedback-page {
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

/* 自定义滚动条 - 仅内部滚动 */
.feedback-list::-webkit-scrollbar {
  width: 4px;
}

.feedback-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.feedback-list::-webkit-scrollbar-thumb {
  background: #c4c4c4;
  border-radius: 4px;
}

.feedback-list::-webkit-scrollbar-thumb:hover {
  background: #a0a0a0;
}

/* 确保Font Awesome图标正常显示 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
</style>