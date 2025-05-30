<template>
  <div class="bg-gray-50 h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-white shadow-sm py-3 px-4 flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <h1 class="font-bold text-gray-800 text-xl">ModelHub <span class="text-gray-400 text-m">V1</span></h1>
      </div>
      <div class="flex space-x-3">
        <button @click="goToLogout" class="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-md hover:shadow-lg">
          <i class="fas fa-sign-out-alt mr-1"></i> Logout
        </button>
        <button @click="goToFeedback" class="ml-4 px-4 py-2 rounded-lg border-2 border-purple-600 text-purple-600 font-medium hover:bg-purple-50 transition-all duration-300">
          <i class="fas fa-comment-alt mr-1"></i> Feedback
        </button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 overflow-hidden flex flex-col">
      <!-- Chat Columns Container -->
      <div class="flex-1 overflow-hidden grid grid-cols-1 md:grid-cols-3 gap-4 p-4">
        <!-- Wenxin Column -->
        <div class="chat-column bg-white rounded-xl shadow-md overflow-hidden flex flex-col h-full">
          <div class="bg-blue-50 px-4 py-3 border-b border-gray-200 flex items-center">
            <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
              <img src="@/assets/文心一言.png" alt="Wenxin Icon" class="w-5 h-5">
            </div>
            <h2 class="font-medium text-gray-700">Wenxin</h2>
          </div>
          <div class="flex-1 overflow-y-auto p-4 message-container" :class="wenxin_messages.length === 0 ? 'empty-state' : ''" ref="messageContainer">
            <div v-for="(message, index) in wenxin_messages" :key="index" class="mb-4">
              <div v-if="message.sender === 'user'" class="flex justify-end mb-2">
                <div class="bg-blue-500 text-white rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg">
                  {{ message.content }}
                </div>
              </div>
              <div v-else class="flex justify-start mb-2">
                <div class="bg-gray-100 rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg ai-response" v-html="message.content"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tongyi Column -->
        <div class="chat-column bg-white rounded-xl shadow-md overflow-hidden flex flex-col h-full">
          <div class="bg-green-50 px-4 py-3 border-b border-gray-200 flex items-center">
            <div class="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center mr-3">
              <img src="@/assets/通义千问.png" alt="Tongyi Icon" class="w-5 h-5">
            </div>
            <h2 class="font-medium text-gray-700">Tongyi</h2>
          </div>
          <div class="flex-1 overflow-y-auto p-4 message-container" :class="tongyi_messages.length === 0 ? 'empty-state' : ''">
            <div v-for="(message, index) in tongyi_messages" :key="index" class="mb-4">
              <div v-if="message.sender === 'user'" class="flex justify-end mb-2">
                <div class="bg-blue-500 text-white rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg">
                  {{ message.content }}
                </div>
              </div>
              <div v-else class="flex justify-start mb-2">
                <div class="bg-gray-100 rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg ai-response" v-html="message.content"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- ChatGPT Column -->
        <div class="chat-column bg-white rounded-xl shadow-md overflow-hidden flex flex-col h-full">
          <div class="bg-purple-50 px-4 py-3 border-b border-gray-200 flex items-center">
            <div class="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center mr-3">
              <img src="@/assets/chatgpt.png" alt="ChatGPT Icon" class="w-5 h-5">
            </div>
            <h2 class="font-medium text-gray-700">ChatGPT</h2>
          </div>
          <div class="flex-1 overflow-y-auto p-4 message-container" :class="chatgpt_messages.length === 0 ? 'empty-state' : ''">
            <div v-for="(message, index) in chatgpt_messages" :key="index" class="mb-4">
              <div v-if="message.sender === 'user'" class="flex justify-end mb-2">
                <div class="bg-blue-500 text-white rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg">
                  {{ message.content }}
                </div>
              </div>
              <div v-else class="flex justify-start mb-2">
                <div class="bg-gray-100 rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg ai-response" v-html="message.content"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="bg-white border-t border-gray-200 px-4 py-3">
        <div class="max-w-4xl mx-auto">
          <div class="relative flex items-center">
            <el-input
                v-model="queryKeyword"
                placeholder="Send a message to all AIs..."
                class="w-full"
                @keyup.enter="handleSearch"
            >
            </el-input>
            <el-button
                v-if="!loading"
                type="primary"
                @click="handleSearch"
                class="absolute right-2 bg-blue-500 text-blue-600 p-2 rounded-lg hover:bg-blue-600"
            >
              <i class="fas fa-paper-plane"></i>
            </el-button>
            <el-button
                v-if="loading"
                type="danger"
                @click="closeEventSource"
                class="absolute right-2 bg-red-500 text-red-600 p-2 rounded-lg hover:bg-red-600"
            >
              <i class="fas fa-stop"></i>
            </el-button>
          </div>
          <p class="text-xs text-gray-500 mt-2 text-center">
            ModelHub may also make mistakes. Please consider checking important information.
          </p>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import MarkdownIt from 'markdown-it';
import markdownItFootnote from 'markdown-it-footnote';
import markdownItTaskLists from 'markdown-it-task-lists';
import markdownItAbbr from 'markdown-it-abbr';
import markdownItContainer from 'markdown-it-container';
import hljs from 'highlight.js';
import markdownItHighlightjs from 'markdown-it-highlightjs';
import router from '../router';

export default {
  name: 'UserDashboard',
  components: {},
  computed: {
    // 将 Markdown 文本渲染为 HTML
    html() {
      return this.md.render(this.message);
    }
  },
  data() {
    return {
      md: new MarkdownIt()
          .use(markdownItFootnote)
          .use(markdownItTaskLists, {enabled: true})
          .use(markdownItAbbr)
          .use(markdownItContainer, 'warning')
          .use(markdownItHighlightjs, {hljs}), // 添加 markdown-it-highlightjs 插件
      queryKeyword: '',
      tempResult: {},
      loading: false,
      wenxin_messages: [],
      tongyi_messages:[],
      chatgpt_messages:[],
      socket: null,
      eventSource: null, // 添加事件源变量
      stopIcon: '@/assets/等待.png',
      uploadIcon: '@/assets/上传.png'
    }
  },
  methods: {
    async handleSearch() {
      // 如果正在加载中，则不执行新的搜索操作
      if (this.loading) {
        return;
      }

      const keyword = this.queryKeyword;
      this.loading = true;
      try {
        let zxakey = "zxa";
        // 初始化一个用于 SSE 的 message 对象
        let wenxin_sseMessage = {
          orgcontent: '',
          content: '',
          sender: 'friend',
          zxakey: zxakey
        };
        let tongyi_sseMessage = {
          orgcontent: '',
          content: '',
          sender: 'friend',
          zxakey: zxakey
        };
        let chatgpt_sseMessage = {
          orgcontent: '',
          content: '',
          sender: 'friend',
          zxakey: zxakey
        };

        this.wenxin_messages.push({
          content: keyword,
          sender: 'user'
        });
        this.tongyi_messages.push({
          content: keyword,
          sender: 'user'
        });
        this.chatgpt_messages.push({
          content: keyword,
          sender: 'user'
        });

        this.$nextTick(() => {
          this.scrollToBottom();
        });

        let wenxin_friendMessage = wenxin_sseMessage;
        // 创建一个新的 EventSource 实例
        this.wenxin_eventSource = new EventSource('/api/wenxin?query=' + keyword);
        // 设置消息事件监听器
        this.wenxin_eventSource.onmessage = (event) => {
          try {
            const dataObject = JSON.parse(event.data);
            // 判断是否为最后一个消息，如果是，则关闭事件源
            if (dataObject.message === 'done') {
              this.wenxin_eventSource.close();
              this.loading = false;
            }
            if (dataObject.message != 'done') {
              // 累加接收到的数据到 friendMessage.orgcontent 中
              wenxin_friendMessage.orgcontent += dataObject.message.toLocaleString();
              wenxin_friendMessage.orgcontent = wenxin_friendMessage.orgcontent.replace(/\*\*\s*([^*]*?)\s*(:\s*)?\*\*/g, '**$1$2**');
              // 更新 friendMessage.content，这里假设 md.render 可以处理累加的字符串
              wenxin_friendMessage.content = this.md.render(wenxin_friendMessage.orgcontent);
            }
            this.scrollToBottom();
          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        };
        this.wenxin_messages.push(wenxin_sseMessage);
        this.queryKeyword = ''; // 清空输入框
        this.wenxin_eventSource.onerror = error => {
          console.error('EventSource failed:', error);
          this.wenxin_eventSource.close();
        };
        let tongyi_friendMessage = tongyi_sseMessage;
        // 创建一个新的 EventSource 实例
        this.tongyi_eventSource = new EventSource('/api/tongyi?query=' + keyword);
        // 设置消息事件监听器
        this.tongyi_eventSource.onmessage = (event) => {
          try {
            const dataObject = JSON.parse(event.data);
            // 判断是否为最后一个消息，如果是，则关闭事件源
            if (dataObject.message === 'done') {
              this.tongyi_eventSource.close();
              this.loading = false;
            }
            if (dataObject.message != 'done') {
              // 累加接收到的数据到 friendMessage.orgcontent 中
              tongyi_friendMessage.orgcontent += dataObject.message.toLocaleString();
              tongyi_friendMessage.orgcontent = tongyi_friendMessage.orgcontent.replace(/\*\*\s*([^*]*?)\s*(:\s*)?\*\*/g, '**$1$2**');
              // 更新 friendMessage.content，这里假设 md.render 可以处理累加的字符串
              tongyi_friendMessage.content = this.md.render(tongyi_friendMessage.orgcontent);
            }
            this.scrollToBottom();
          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        };
        this.tongyi_messages.push(tongyi_sseMessage);
        this.queryKeyword = ''; // 清空输入框
        this.tongyi_eventSource.onerror = error => {
          console.error('EventSource failed:', error);
          this.tongyi_eventSource.close();
        };
        let chatgpt_friendMessage = chatgpt_sseMessage;
        // 创建一个新的 EventSource 实例
        this.chatgpt_eventSource = new EventSource('/api/chatgpt?query=' + keyword);
        // 设置消息事件监听器
        this.chatgpt_eventSource.onmessage = (event) => {
          try {
            const dataObject = JSON.parse(event.data);
            // 判断是否为最后一个消息，如果是，则关闭事件源
            if (dataObject.message === 'done') {
              this.chatgpt_eventSource.close();
              this.loading = false;
            }
            if (dataObject.message != 'done') {
              // 累加接收到的数据到 friendMessage.orgcontent 中
              chatgpt_friendMessage.orgcontent += dataObject.message.toLocaleString();
              chatgpt_friendMessage.orgcontent = chatgpt_friendMessage.orgcontent.replace(/\*\*\s*([^*]*?)\s*(:\s*)?\*\*/g, '**$1$2**');
              // 更新 friendMessage.content，这里假设 md.render 可以处理累加的字符串
              chatgpt_friendMessage.content = this.md.render(chatgpt_friendMessage.orgcontent);
            }
            this.scrollToBottom();
          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        };
        this.chatgpt_messages.push(chatgpt_sseMessage);
        this.queryKeyword = ''; // 清空输入框
        this.chatgpt_eventSource.onerror = error => {
          console.error('EventSource failed:', error);
          this.chatgpt_eventSource.close();
        };

      } catch (error) {
        console.error('发送消息时出错：', error);
      } finally {
      }
    },
    closeEventSource() {
      this.loading = false;
      if (this.eventSource) {
        this.eventSource.close();
      }
    },
    scrollToBottom() {
      const messageContainer = this.$refs.messageContainer;
      if (messageContainer) {
        messageContainer.scrollTop = messageContainer.scrollHeight;
      }
    },
    beforeDestroy() {
      if (this.eventSource) {
        this.eventSource.close();
      }
    },
    goToLogout() {
      router.push({ name: 'Logout' });
    },
    goToFeedback(){
      router.push({ name: 'Feedback'});
    }
  },
}
</script>

<style scoped>
.message-container {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

.message-container::-webkit-scrollbar {
  width: 6px;
}

.message-container::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.message-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.message-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.ai-response pre {
  background-color: #f8f8f8;
  border-radius: 8px;
  padding: 12px;
  overflow-x: auto;
  margin: 8px 0;
}

.ai-response code {
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
}

.ai-response p {
  margin-bottom: 12px;
  line-height: 1.6;
}

.ai-response ul, .ai-response ol {
  margin-left: 20px;
  margin-bottom: 12px;
}

.ai-response li {
  margin-bottom: 6px;
}

.empty-state {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 24 24" fill="none" stroke="%23e5e7eb" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>');
  background-repeat: no-repeat;
  background-position: center;
  background-size: 30%;
  opacity: 0.5;
}

.chat-column {
  transition: all 0.3s ease;
}

.chat-column:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.send-button {
  transition: all 0.2s ease;
}

.send-button:hover {
  transform: scale(1.05);
}

.send-button:active {
  transform: scale(0.95);
}

/* 覆盖Element UI样式 */
:deep(.el-input__inner) {
  height: 48px;
  border-radius: 12px;
  padding-right: 50px;
}

:deep(.el-button) {
  border: none;
  background: transparent;
}
</style>