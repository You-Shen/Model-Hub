<template>
  <div class="user-settings-page bg-grid-pattern">
    <!-- 顶部导航栏 -->
    <header class="bg-white/90 shadow-sm backdrop-blur-md sticky top-0 z-50">
      <div class="container mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center space-x-2">
          <i class="fas fa-robot text-purple-600 text-xl"></i>
          <span class="font-bold text-gray-800 text-xl">ModelHub <span class="text-gray-400 text-m">V2</span></span>
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
    <main class="container mx-auto px-4 py-8">
      <div class="settings-card bg-white rounded-2xl shadow-xl p-8">
        <div class="flex flex-col items-center mb-8">
          <i class="fas fa-cog text-purple-600 text-4xl mb-3"></i>
          <h2 class="text-2xl font-bold text-gray-800">用户偏好设置</h2>
          <p class="text-gray-500">自定义您的AI交互体验</p>
        </div>

        <!-- 设置表单 -->
        <form @submit.prevent="saveSettings" class="space-y-6">
          <!-- Prompt设置 -->
          <div class="setting-group">
            <label class="setting-label">
              <i class="fas fa-comment-dots mr-2 text-purple-500"></i>
              系统Prompt
            </label>
            <textarea
                v-model="settings.prompt"
                class="setting-input"
                rows="4"
                placeholder="请输入您希望AI遵循的系统级提示词..."
            ></textarea>
            <p class="setting-hint">这将影响AI与您交互的基本方式</p>
          </div>

          <!-- 温度设置 -->
          <div class="setting-group">
            <label class="setting-label">
              <i class="fas fa-thermometer-half mr-2 text-purple-500"></i>
              模型输出温度 (Temperature)
            </label>
            <div class="flex items-center space-x-4">
              <input
                  v-model.number="settings.temperature"
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-purple-500"
              >
              <span class="text-sm font-medium text-gray-700 w-12 text-right">{{ settings.temperature }}</span>
            </div>
            <p class="setting-hint">数值越高，AI输出越随机；数值越低，结果越确定。</p>
          </div>


          <!-- 模型优先级 -->
          <div class="setting-group">
            <label class="setting-label">
              <i class="fas fa-layer-group mr-2 text-purple-500"></i>
              模型选择
            </label>
            <div class="model-priority-grid grid grid-cols-1 md:grid-cols-3 gap-4">
              <div
                  v-for="model in availableModels"
                  :key="model.id"
                  class="model-option p-4 rounded-lg border-2 cursor-pointer transition-all"
                  :class="{
                    'border-purple-500 bg-purple-50': settings.modelPriority.includes(model.id),
                    'border-gray-200 hover:border-purple-300': !settings.modelPriority.includes(model.id)
                  }"
                  @click="toggleModelPriority(model.id)"
              >
                <div class="flex items-center">
                  <i class="fas text-purple-600 mr-3" :class="model.icon"></i>
                  <div>
                    <h3 class="font-medium">{{ model.name }}</h3>
                    <p class="text-xs text-gray-500">{{ model.description }}</p>
                  </div>
                </div>
              </div>
            </div>
            <p class="setting-hint">点击模型卡片可确定是否使用该模型</p>
          </div>

          <!-- 操作按钮 -->
          <div class="flex justify-end space-x-4 pt-6">
            <button
                type="button"
                @click="resetSettings"
                class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition"
            >
              恢复默认
            </button>
            <button
                type="submit"
                class="px-6 py-2 rounded-lg bg-gradient-to-r from-purple-600 to-blue-500 text-white font-medium hover:from-purple-700 hover:to-blue-600 transition shadow-md"
            >
              确认设置
            </button>
          </div>
        </form>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer bg-white/80 backdrop-blur-md">
      <div class="container mx-auto px-4 py-4">
        <div class="text-center text-xs text-gray-500">
          ©2025 Created by ModelHub V2 team. All rights reserved.
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'; // 引入 axios
import router from '../router';
export default {
  name: 'UserSettings',
  data() {
    return {
      settings: {
        prompt: '你是一个助手...',
        temperature: 0.7,
        modelPriority: ['gpt', 'wenxin', 'tongyi']
      },
      availableModels: [
        {
          id: 'gpt',
          name: 'GPT',
          description: 'OpenAI最新模型，强大的多任务处理能力',
          icon: 'fa-brain'
        },
        {
          id: 'wenxin',
          name: '文心一言',
          description: '百度中文大模型',
          icon: 'fa-search'
        },
        {
          id: 'tongyi',
          name: '通义千问',
          description: '通义千问大模型',
          icon: 'fa-comments'
        }
      ]
    };
  },
  mounted() { //生命周期钩子：组件挂载完成后执行
    this.fetchSettings();
  },
  methods: {
    goBack() {
      router.push({ name: 'UserDashboard'});
    },
    toggleModelPriority(modelId) {
      if (this.settings.modelPriority.includes(modelId)) {
        this.settings.modelPriority = this.settings.modelPriority.filter(id => id !== modelId);
      } else {
        this.settings.modelPriority.push(modelId);
      }
    },
    async fetchSettings() { //新增方法：获取设置
      try {
        const res = await axios.get('/api/user/settings');
        this.settings = {
          prompt: res.data.prompt || '你是一个助手...',
          temperature: res.data.temperature || 0.7,
          modelPriority: res.data.model_priority || ['gpt', 'wenxin', 'tongyi']
        };
      } catch (error) {
        console.error('获取设置失败:', error);
        this.$message.error('无法加载设置，请刷新重试');
      }
    },
    async saveSettings() { //提交保存的方法
      try {
        const res = await axios.post('/api/user/settings', {
          prompt: this.settings.prompt,
          temperature: this.settings.temperature,
          model_priority: this.settings.modelPriority
        });

        if (res.status === 200) {
          this.$message.success('设置已保存');
        }
      } catch (error) {
        console.error('保存设置失败:', error);
        this.$message.error('保存失败，请重试');
      }
    },
    resetSettings() {
      this.settings = {
        prompt: '你是一个助手...',
        temperature: 0.7,
        modelPriority: ['gpt', 'wenxin', 'tongyi']
      };
      this.$message.info('已恢复默认设置');
    }
  }
};
</script>

<style scoped>
.user-settings-page {
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

.settings-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.settings-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.setting-group {
  @apply space-y-2;
}

.setting-label {
  @apply flex items-center text-gray-700 font-medium text-sm;
}

.setting-input {
  @apply w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-purple-500 focus:ring-1 focus:ring-purple-200 transition;
}

.setting-hint {
  @apply text-xs text-gray-500;
}

.model-option {
  transition: all 0.2s ease;
}

.model-option:hover {
  transform: translateY(-2px);
}
/* 自定义 range input 样式 */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px; /* 轨道高度 */
  background: transparent; /* 背景透明，使用轨道样式 */
  border-radius: 8px; /* 圆角 */
  cursor: pointer;
}

/* 轨道样式（更淡的紫色） */
input[type="range"]::-webkit-slider-runnable-track {
  width: 100%;
  height: 6px;
  background: linear-gradient(to right, #a855f740, #6366f140); /* 更淡的紫色（添加透明度） */
  border-radius: 8px;
}

input[type="range"]::-moz-range-track {
  width: 100%;
  height: 6px;
  background: linear-gradient(to right, #a855f740, #6366f140); /* 更淡的紫色（添加透明度） */
  border-radius: 8px;
}

/* 滑块样式（修正位置） */
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: linear-gradient(to right, #a855f7, #6366f1); /* 紫色渐变 */
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  margin-top: -5px; /* 修正垂直居中（根据滑块和轨道高度调整） */
}

input[type="range"]::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: linear-gradient(to right, #a855f7, #6366f1); /* 紫色渐变 */
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  margin-top: -5px; /* 修正垂直居中（根据滑块和轨道高度调整） */
}

/* 悬停放大效果 */
input[type="range"]:hover::-webkit-slider-thumb {
  transform: scale(1.2);
}

input[type="range"]:hover::-moz-range-thumb {
  transform: scale(1.2);
}

/* 确保Font Awesome图标正常显示 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
</style>