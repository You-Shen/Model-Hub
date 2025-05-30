<!--<template>-->
<!--  <div class="feedback-background">-->
<!--    &lt;!&ndash; 顶部栏 &ndash;&gt;-->
<!--    <div class="top-bar">-->
<!--      <div class="left">-->
<!--        <span>ChatWithAIs V1 | 一站式大语言模型访问平台</span>-->
<!--      </div>-->
<!--      <div class="right">-->
<!--        <button @click="goBack" class="home-link">返回</button>-->
<!--      </div>-->
<!--    </div>-->

<!--    <div class="feedback-container">-->
<!--      <div class="feedback-form">-->
<!--        <h2>用户反馈</h2>-->
<!--        <form @submit.prevent="submitFeedback">-->
<!--          <textarea v-model="feedback" placeholder="请输入您的反馈..." required></textarea>-->
<!--          <button type="submit">提交反馈</button>-->
<!--        </form>-->
<!--        <p>{{ feedbackMessage }}</p>-->
<!--      </div>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--import axios from 'axios';-->
<!--import router from "@/router";-->
<!--axios.defaults.withCredentials = true;-->
<!--export default {-->
<!--  name: 'Feedback',-->
<!--  data() {-->
<!--    return {-->
<!--      feedback: '',-->
<!--      feedbackMessage: ''-->
<!--    };-->
<!--  },-->
<!--  methods: {-->
<!--    async submitFeedback() {-->
<!--      try {-->
<!--        await axios.post('/api/user/feedback', {-->
<!--          message: this.feedback // 使用正确的字段名-->
<!--        },{ withCredentials: true });-->
<!--        this.feedbackMessage = '反馈提交成功！感谢您的反馈。';-->
<!--        this.feedback = ''; // 清空反馈-->
<!--      } catch (error) {-->
<!--        this.feedbackMessage = '反馈提交失败，请稍后重试。';-->
<!--        console.error('Feedback submission error:', error);-->
<!--      }-->
<!--    },-->
<!--    goBack() {-->
<!--      // 返回到之前的对话页面的逻辑-->
<!--      router.push({ name: 'UserDashboard' });-->
<!--    }-->
<!--  }-->
<!--};-->
<!--</script>-->

<!--<style scoped>-->
<!--.feedback-background {-->
<!--  background-image: url('@/assets/feedback.png');-->
<!--  background-size: cover;-->
<!--  background-position: center;-->
<!--  height: 100vh;-->
<!--  display: flex;-->
<!--  flex-direction: column;-->
<!--}-->

<!--.top-bar {-->
<!--  display: flex;-->
<!--  justify-content: space-between;-->
<!--  align-items: center;-->
<!--  background-color: #D6EAF8;-->
<!--  padding: 10px;-->
<!--  color: #1296db;-->
<!--  height: 35px;-->
<!--  font-weight: bold;-->
<!--}-->

<!--.top-bar .left {-->
<!--  font-size: 20px;-->
<!--}-->

<!--.top-bar .right button {-->
<!--  margin-left: 0px;-->
<!--  padding: 8px 16px;-->
<!--  background-color: #ffffff;-->
<!--  color: #1296db;-->
<!--  border-radius: 5px;-->
<!--  cursor: pointer;-->
<!--  transition: background-color 0.3s, color 0.3s;-->
<!--  font-weight: bold;-->
<!--}-->

<!--.top-bar .right button:hover {-->
<!--  background-color: #1296db;-->
<!--  color: #ffffff;-->
<!--}-->

<!--.feedback-container {-->
<!--  flex: 1;-->
<!--  display: flex;-->
<!--  justify-content: center;-->
<!--  align-items: center;-->
<!--}-->

<!--.feedback-form {-->
<!--  width: 400px;-->
<!--  max-width: 90%;-->
<!--  background-color: rgba(255, 255, 255, 0.9);-->
<!--  padding: 20px;-->
<!--  border-radius: 10px;-->
<!--  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);-->
<!--}-->

<!--.feedback-form h2 {-->
<!--  margin-bottom: 20px;-->
<!--  text-align: center;-->
<!--}-->

<!--textarea {-->
<!--  width: calc(100% - 40px);-->
<!--  height: 150px;-->
<!--  margin: 0 auto 20px auto;-->
<!--  padding: 10px;-->
<!--  border: 1px solid #ccc;-->
<!--  border-radius: 5px;-->
<!--  resize: vertical;-->
<!--  display: block;-->
<!--}-->

<!--button {-->
<!--  width: 100%;-->
<!--  padding: 10px;-->
<!--  background-color: #1296db;-->
<!--  color: #fff;-->
<!--  border: none;-->
<!--  border-radius: 5px;-->
<!--  font-size: 16px;-->
<!--  cursor: pointer;-->
<!--  transition: background-color 0.3s ease;-->
<!--}-->

<!--button:hover {-->
<!--  background-color: #0056b3;-->
<!--}-->

<!--.feedback-form p {-->
<!--  margin-top: 10px;-->
<!--  font-size: 14px;-->
<!--  color: #ff0000;-->
<!--}-->
<!--</style>-->
<template>
  <div class="feedback-page bg-grid-pattern">
    <!-- 顶部导航栏 -->
    <header class="bg-white/90 shadow-sm backdrop-blur-md sticky top-0 z-50">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <i class="fas fa-robot text-purple-600 text-xl"></i>
          <span class="font-bold text-gray-800 text-xl">ModelHub <span class="gradient-text">V1</span></span>
          <span class="hidden md:inline text-sm text-gray-500 ml-2">一站式大语言模型访问平台</span>
        </div>
        <button
            @click="goBack"
            class="ml-6 px-4 py-2 rounded-lg border-2 border-purple-600 text-purple-600 font-medium hover:bg-purple-50 transition-all duration-300"
        >
          返回
        </button>
      </div>
    </header>

    <!-- 反馈表单 -->
    <main class="container mx-auto px-4 py-8 flex justify-center items-center flex-1">
      <div class="feedback-card bg-white rounded-2xl shadow-lg p-8 w-full max-w-md">
        <div class="text-center mb-6">
          <i class="fas fa-comment-dots text-purple-600 text-4xl mb-3"></i>
          <h2 class="text-2xl font-bold text-gray-800">用户反馈</h2>
          <p class="text-gray-500 mt-1">您的意见对我们非常重要</p>
        </div>

        <form @submit.prevent="submitFeedback" class="space-y-4">
          <div>
            <textarea
                v-model="feedback"
                placeholder="请告诉我们您的想法或遇到的问题..."
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                rows="5"
                required
            ></textarea>
          </div>

          <button
              type="submit"
              class="w-full px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-md hover:shadow-lg"
          >
            提交反馈
          </button>
        </form>

        <p
            v-if="feedbackMessage"
            class="mt-4 text-center"
            :class="feedbackMessage.includes('成功') ? 'text-green-600' : 'text-red-600'"
        >
          {{ feedbackMessage }}
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
axios.defaults.withCredentials = true;
export default {
  name: 'Feedback',
  data() {
    return {
      feedback: '',
      feedbackMessage: ''
    };
  },
  methods: {
    async submitFeedback() {
      try {
        await axios.post('/api/user/feedback', {
          message: this.feedback // 使用正确的字段名
        },{ withCredentials: true });
        this.feedbackMessage = '反馈提交成功！感谢您的反馈。';
        this.feedback = ''; // 清空反馈
      } catch (error) {
        this.feedbackMessage = '反馈提交失败，请稍后重试。';
        console.error('Feedback submission error:', error);
      }
    },
    goBack() {
      // 返回到之前的对话页面的逻辑
      router.push({ name: 'UserDashboard' });
    }
  }
};
</script>

<style scoped>
.feedback-page {
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

.feedback-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feedback-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

textarea {
  resize: vertical;
  min-height: 120px;
}

/* 确保Font Awesome图标正常显示 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
</style>