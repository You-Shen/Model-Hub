<template>
  <div class="home bg-grid-pattern" >
    <!-- 顶部导航栏 -->
    <header class="bg-white/90 shadow-sm backdrop-blur-md sticky top-0 z-50">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <i class="fas fa-robot text-purple-600 text-xl"></i>
          <span class="font-bold text-gray-800 text-xl">ModelHub <span class="gradient-text">V1</span></span>
          <span class="hidden md:inline text-sm text-gray-500 ml-2">一站式大语言模型访问平台</span>
        </div>
        <div class="flex items-center space-x-4">
          <router-link
              to="/login"
              class="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-md hover:shadow-lg"
          >
            登录
          </router-link>
          <router-link
              to="/register"
              class="ml-4 px-4 py-2 rounded-lg border-2 border-purple-600 text-purple-600 font-medium hover:bg-purple-50 transition-all duration-300"
          >
            注册
          </router-link>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="container mx-auto px-4 py-8">
      <!-- 轮播图部分 -->
      <div class="carousel-container">
        <div class="carousel">
          <div
              class="carousel-item"
              v-for="(image, index) in images"
              :key="index"
              :class="{ active: currentIndex === index }"
              :style="getCarouselItemStyle(index)"
          >
            <h2 class="text-4xl font-bold">{{ getCarouselTitle(index) }}</h2>
            <div class="carousel-caption" v-html="image.caption"></div>
          </div>
          <button class="carousel-control prev" @click="prevSlide">&#10094;</button>
          <button class="carousel-control next" @click="nextSlide">&#10095;</button>
        </div>

        <!-- 指示点 -->
        <div class="dots">
          <span
              v-for="(image, index) in images"
              :key="index"
              :class="{ active: currentIndex === index }"
              @click="goToSlide(index)"
          ></span>
        </div>
      </div>

      <!-- 特性展示 -->
      <section class="mt-16">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-12">核心特性</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="feature-card">
            <div class="text-purple-600 text-4xl mb-4">
              <i class="fas fa-bolt"></i>
            </div>
            <h3 class="text-xl font-bold mb-2">快速响应</h3>
            <p class="text-gray-600">优化的AI模型响应机制，确保您获得最快的回答</p>
          </div>
          <div class="feature-card">
            <div class="text-blue-500 text-4xl mb-4">
              <i class="fas fa-shield-alt"></i>
            </div>
            <h3 class="text-xl font-bold mb-2"> 数据私密</h3>
            <p class="text-gray-600">采用端到端加密技术，保障用户输入内容的隐私和模型调用过程的安全。</p>
          </div>
          <div class="feature-card">
            <div class="text-green-500 text-4xl mb-4">
              <i class="fas fa-cogs"></i>
            </div>
            <h3 class="text-xl font-bold mb-2">高度可定制</h3>
            <p class="text-gray-600">支持模型选择、结果排序及展示样式定制，打造个性化的大模型使用体验。</p>
          </div>
        </div>
      </section>

      <!-- 模型展示 -->
      <section class="mt-20 bg-white rounded-2xl p-8 shadow-lg">
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-8">支持的AI模型</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="flex flex-col items-center p-4 hover:bg-gray-50 rounded-xl transition">
            <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mb-3">
              <img src="@/assets/chatgpt.png" alt="ChatGPT Icon" class="w-10 h-10">
            </div>
            <span class="font-medium">GPT-4</span>
          </div>
          <div class="flex flex-col items-center p-4 hover:bg-gray-50 rounded-xl transition">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-3">
              <img src="@/assets/通义千问.png" alt="Tongyi Icon" class="w-10 h-10">
            </div>
            <span class="font-medium">Qwen</span>
          </div>
          <div class="flex flex-col items-center p-4 hover:bg-gray-50 rounded-xl transition">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-3">
              <img src="@/assets/文心一言.png" alt="Wenxin Icon" class="w-10 h-10">
            </div>
            <span class="font-medium">文心</span>
          </div>
          <div class="flex flex-col items-center p-4 hover:bg-gray-50 rounded-xl transition">
            <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mb-3">
              <i class="fas fa-lightbulb text-yellow-600 text-2xl"></i>
            </div>
            <span class="font-medium">其他</span>
          </div>
        </div>
      </section>
    </main>

    <!-- 页脚 -->
    <footer class="footer bg-white/80 backdrop-blur-md mt-12">
      <div class="container mx-auto px-4 py-6">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="flex items-center space-x-2 mb-4 md:mb-0">
            <i class="fas fa-robot text-purple-600 text-xl"></i>
            <span class="font-bold text-gray-800">ModelHub</span>
          </div>
          <div class="flex space-x-6">
            <a href="#" class="text-gray-500 hover:text-purple-600 transition">关于我们</a>
            <a href="#" class="text-gray-500 hover:text-purple-600 transition">隐私政策</a>
            <a href="#" class="text-gray-500 hover:text-purple-600 transition">服务条款</a>
            <a href="#" class="text-gray-500 hover:text-purple-600 transition">联系我们</a>
          </div>
        </div>
        <div class="mt-6 text-center text-sm text-gray-500">
          ©2025 Created by HIT-ModelHub team. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      images: [
        {
          // src: require('../assets/homepage1.png'),
          alt: 'homepage1',
          caption: '打造多大语言模型集成的智能助手平台，<br>为用户提供一站式信息查询服务。'
        },
        {
          // src: require('../assets/homepage2.png'),
          alt: 'homepage2',
          caption: '实现一站式大语言模型访问，<br>支持ChatGPT、文心一言、通义千问。'
        },
        {
          // src: require('../assets/homepage3.png'),
          alt: 'homepage3',
          caption: '关注系统的长期运行和维护，<br>确保系统为用户提供稳定、优质的服务。'
        },
      ],
      currentIndex: 0,
      intervalId: null,
      carouselTitles: [
        '探索AI的无限可能',
        '多模型自由切换',
        '开发者友好'
      ],
      carouselStyles: [
        { background: 'linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%)', color: 'white' },
        { background: 'linear-gradient(135deg, #10b981 0%, #3b82f6 100%)', color: 'white' },
        { background: 'linear-gradient(135deg, #f9fafb 0%, #e5e7eb 100%)', color: '#111827' }
      ]
    };
  },
  mounted() {
    this.startCarousel();
  },
  methods: {
    startCarousel() {
      this.intervalId = setInterval(() => {
        this.nextSlide();
      }, 5000);
    },
    nextSlide() {
      this.currentIndex = (this.currentIndex + 1) % this.images.length;
    },
    prevSlide() {
      this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
    },
    goToSlide(index) {
      this.currentIndex = index;
    },
    getCarouselTitle(index) {
      return this.carouselTitles[index] || '';
    },
    getCarouselItemStyle(index) {
      return this.carouselStyles[index] || {};
    }
  },
  beforeDestroy() {
    clearInterval(this.intervalId);
  }
};
</script>

<style scoped>
:root {
  --primary: #8b5cf6;
  --primary-dark: #7c3aed;
  --secondary: #3b82f6;
}

.bg-grid-pattern {
  background-image:
      linear-gradient(to right, rgba(0, 0, 0, 0.03) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(0, 0, 0, 0.03) 1px, transparent 1px);
  background-size: 20px 20px;
  min-height: 100vh;
}

.gradient-text {
  background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.carousel-container {
  position: relative;
  max-width: 1500px;
  margin: 2rem auto;
  border-radius: 1.5rem;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.carousel {
  position: relative;
  width: 100%;
  height: 400px;
  overflow: hidden;
}

.carousel-item {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 0.5s ease-in-out;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  text-align: center;
}

.carousel-item.active {
  opacity: 1;
}

.carousel-caption {
  max-width: 800px;
  font-size: 1.5rem;
  line-height: 1.5;
  margin-top: 1.5rem;
}

.carousel-control {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.3);
  color: white;
  border: none;
  padding: 1rem;
  cursor: pointer;
  font-size: 1.5rem;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(5px);
  transition: all 0.3s ease;
}

.carousel-control:hover {
  background: rgba(255, 255, 255, 0.5);
}

.carousel-control.prev {
  left: 2rem;
}

.carousel-control.next {
  right: 2rem;
}

.dots {
  position: absolute;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
}

.dots span {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}

.dots span.active {
  background: white;
  transform: scale(1.2);
}

.feature-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 确保Font Awesome图标正常显示 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
</style>