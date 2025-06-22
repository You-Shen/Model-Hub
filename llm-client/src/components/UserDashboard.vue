<template>
  <div class="bg-gray-50 h-screen flex">
    <!-- 侧边栏 -->
    <div class="sidebar bg-white shadow-md w-64 flex flex-col">
      <div class="sidebar-header p-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">历史聊天记录</h2>
        <el-button
            type="primary"
            icon="el-icon-edit"
            @click="CreateNewAndSave"
            class="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white"
        >
          创建并保存
        </el-button>
      </div>

      <!-- 聊天记录列表 -->
      <div class="sidebar-list flex-1 overflow-y-auto p-2">
        <ul>
          <li v-for="(theme, index) in themes" :key="index" class="mb-2">
            <div
                :class="{
                'theme-container flex items-center justify-between p-2 rounded-lg hover:bg-gray-100 transition': true,
                'bg-blue-50': theme.id === current_id
              }"
            >
              <a
                  :href="'#'+theme.id"
                  class="truncate-text text-gray-700 hover:text-blue-600 flex-1"
                  @click.prevent="get_conversation(theme.id)"
              >
                {{ theme.summary }}
              </a>
              <el-button
                  type="danger"
                  icon="el-icon-delete"
                  @click="deleteConversation(theme.id)"
                  class="!p-2 !ml-2"
                  circle
              ></el-button>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- 顶部栏 -->
      <header class="bg-white shadow-sm py-3 px-4 flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <h1 class="font-bold text-gray-800 text-xl">ModelHub <span class="text-gray-400 text-m">V2</span></h1>
        </div>
        <div class="flex space-x-3">
          <button
              @click="goToLogout"
              class="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 text-white font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-md hover:shadow-lg"
          >
            <i class="fas fa-sign-out-alt mr-1"></i> 登出
          </button>
          <button
              @click="goToFeedback"
              class="ml-4 px-4 py-2 rounded-lg border-2 border-purple-600 text-purple-600 font-medium hover:bg-purple-50 transition-all duration-300"
          >
            <i class="fas fa-comment-alt mr-1"></i> 反馈
          </button>
          <button
              @click="goToSetting"
              class="px-4 py-2 rounded-lg bg-gradient-to-r from-purple-500 to-indigo-600 text-white font-medium hover:from-purple-600 hover:to-indigo-700 transition-all duration-300 shadow-md hover:shadow-lg flex items-center"
          >
            <i class="fas fa-cog mr-1"></i> 设置
          </button>
        </div>
      </header>

      <!-- 聊天区域 -->
      <main class="flex-1 overflow-hidden flex flex-col bg-gray-100">
        <!-- 三列聊天容器 -->
        <div class="flex-1 overflow-hidden grid grid-cols-1 md:grid-cols-3 gap-4 p-4">
          <!-- 文心一言列 -->
          <div class="chat-column bg-white rounded-xl shadow-md overflow-hidden flex flex-col h-full">
            <div class="bg-blue-50 px-4 py-3 border-b border-gray-200 flex items-center">
              <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                <img src="@/assets/文心一言.png" alt="Wenxin Icon" class="w-5 h-5">
              </div>
              <h2 class="font-medium text-gray-700">文心一言</h2>
            </div>
            <div
                class="flex-1 overflow-y-auto p-4 message-container"
                :class="wenxin_messages.length === 0 ? 'empty-state' : ''"
                ref="messageContainer0"
            >
              <div v-for="(message, index) in wenxin_messages" :key="index" class="mb-4">
                <div v-if="message.role === 'user'" class="flex justify-end mb-2">
                  <div class="bg-blue-500 text-white rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg">
                    {{ message.content }}
                  </div>
                </div>
                <div v-else class="flex justify-start mb-2">
                  <div class="bg-gray-100 rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg ai-response" v-html="renderMessage(message.content,message)"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- 通义千问列 -->
          <div class="chat-column bg-white rounded-xl shadow-md overflow-hidden flex flex-col h-full">
            <div class="bg-green-50 px-4 py-3 border-b border-gray-200 flex items-center">
              <div class="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center mr-3">
                <img src="@/assets/通义千问.png" alt="Tongyi Icon" class="w-5 h-5">
              </div>
              <h2 class="font-medium text-gray-700">通义千问</h2>
            </div>
            <div
                class="flex-1 overflow-y-auto p-4 message-container"
                :class="tongyi_messages.length === 0 ? 'empty-state' : ''"
                ref="messageContainer1"
            >
              <div v-for="(message, index) in tongyi_messages" :key="index" class="mb-4">
                <div v-if="message.role === 'user'" class="flex justify-end mb-2">
                  <div class="bg-blue-500 text-white rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg">
                    {{ message.content }}
                  </div>
                </div>
                <div v-else class="flex justify-start mb-2">
                  <div class="bg-gray-100 rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg ai-response" v-html="renderMessage(message.content,message)"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- ChatGPT列 -->
          <div class="chat-column bg-white rounded-xl shadow-md overflow-hidden flex flex-col h-full">
            <div class="bg-purple-50 px-4 py-3 border-b border-gray-200 flex items-center">
              <div class="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center mr-3">
                <img src="@/assets/chatgpt.png" alt="ChatGPT Icon" class="w-5 h-5">
              </div>
              <h2 class="font-medium text-gray-700">ChatGPT</h2>
            </div>
            <div
                class="flex-1 overflow-y-auto p-4 message-container"
                :class="chatgpt_messages.length === 0 ? 'empty-state' : ''"
                ref="messageContainer2"
            >
              <div v-for="(message, index) in chatgpt_messages" :key="index" class="mb-4">
                <div v-if="message.role === 'user'" class="flex justify-end mb-2">
                  <div class="bg-blue-500 text-white rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg">
                    {{ message.content }}
                  </div>
                </div>
                <div v-else class="flex justify-start mb-2">
                  <div class="bg-gray-100 rounded-lg py-2 px-4 max-w-xs md:max-w-md lg:max-w-lg ai-response" v-html="renderMessage(message.content,message)"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="bg-white border-t border-gray-200 px-4 py-3">
          <div class="max-w-4xl mx-auto">
            <div class="relative flex items-center">
              <el-input
                  v-model="queryKeyword"
                  placeholder="给大模型发送消息"
                  class="w-full"
                  @keyup.enter="handleSearch"
              >
              </el-input>
              <el-button
                  v-if="!loading"
                  type="primary"
                  @click="handleSearch"
                  :disabled="!queryKeyword.trim()"
                  class="absolute right-2 bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600"
              >
                <i class="fas fa-paper-plane"></i>
              </el-button>
              <el-button
                  v-if="loading"
                  type="danger"
                  @click="closeEventSource"
                  class="absolute right-2 bg-red-500 text-white p-2 rounded-lg hover:bg-red-600"
              >
                <i class="fas fa-stop"></i>
              </el-button>
              <input
                  type="file"
                  accept="image/*"
                  @change="handleImageUpload"
                  class="hidden"
                  id="imageUploadInput"
              />
              <!-- 图片上传按钮（样式与发送按钮一致） -->
              <el-button
                  type="primary"
                  class="absolute right-12 bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600"
              >
                <label for="imageUploadInput" class="cursor-pointer">
                  <i class="fas fa-upload"></i>
                </label>
              </el-button>
            </div>
            <p class="text-xs text-gray-500 mt-2 text-center">
              ModelHub may also make mistakes. Please consider checking important information.
            </p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
import MarkdownIt from 'markdown-it';
import markdownItFootnote from 'markdown-it-footnote';
import markdownItTaskLists from 'markdown-it-task-lists';
import markdownItAbbr from 'markdown-it-abbr';
import markdownItContainer from 'markdown-it-container';
import hljs from 'highlight.js';
import axios from 'axios';
import markdownItHighlightjs from 'markdown-it-highlightjs';
import router from '../router';

export default {
  name: 'UserDashboard',
  components: {},
  computed: {
    // 将 Markdown 文本渲染为 HTML
    html() {
      return this.md.render(this.messages);
    },
  },
  data() {
    return {
      md: new MarkdownIt()
          .use(markdownItFootnote)
          .use(markdownItTaskLists, {enabled: true})
          .use(markdownItAbbr)
          .use(markdownItContainer, 'warning')
          .use(markdownItHighlightjs, {hljs}), // 添加 markdown-it-highlightjs 插件
      current_id: null,
      queryKeyword: '',
      tempResult: {},
      flag:0,
      loading: false,
      wenxin_messages: [],
      tongyi_messages:[],
      chatgpt_messages:[],
      socket: null,
      eventSource: null, // 添加事件源变量
      stopIcon: '@/assets/等待.png',
      uploadIcon: '@/assets/上传.png',
      themes: [], // 存储从数据库中获取的主题列表
      uploadedImages: [], // 存储已上传的 Base64 图片数据
      parsedTextFromImage: '', // 图片解析后的文本
    }
  },
  created() {
    // 在组件实例化后立即运行一次 fetchThemes()
    this.fetchThemes();
    //this.get_conversation(-1);
  },
  methods: {

    get_conversation(themeId){
      this.flag=0;
      this.current_id=themeId;
      // 发起 HTTP GET 请求到后端路由 /conversations/get_conversation
      fetch(`/api/conversations/get_conversation?id=${themeId}`, {
        method: 'GET',
        credentials: 'include' // 如果使用会话进行身份验证，则包括 cookies
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            // 过滤掉 role === 'system' 的消息
            this.chatgpt_messages = data.chatgpt_messages.filter(msg => msg.role !== 'system');
            this.tongyi_messages = data.tongyi_messages.filter(msg => msg.role !== 'system');
            this.wenxin_messages = data.wenxin_messages.filter(msg => msg.role !== 'system');
          })
          .catch(error => {
            // 处理错误情况
            console.error('Error:', error.message);
          });
    },

    fetchThemes() {
      // 发起 GET 请求到后端路由
      fetch('/api/conversations/get_conversation_summary', {
        method: 'GET',
        credentials: 'include' // Include cookies if using sessions for authentication
      })
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            // 在这里处理返回的聊天记录数据
            // 假设返回的数据格式为 [{ id: 1, summary: '主题1' }, { id: 2, summary: '主题2' }, ...]
            this.themes = data;
          })
          .catch(error => {
            console.error('Error:', error.message);
          });
    },
    //对话id一定是在保存时在后端设置的，所以前端创建新对话时id设置为null
    //假如当前id不为null，那么就是旧对话，应该更新相应对话id的内容，而不是增加保存记录
    //假如当前id为null，那么就是新对话，增加保存记录
    CreateNewAndSave() {
      if (this.current_id == null) {
        // 如果当前ID为null，创建新对话
        fetch('/api/conversations/new_conversation', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        })
            .then(response => {
              if (!response.ok) {
                throw new Error('Failed to create and save conversation');
              }
              return response.json();
            })
            .then(data => {
              alert('Conversation created and saved successfully.');
              this.messages_chatgpt = [];

              this.messages_tongyi = [];
              this.messages_wenxin = [];
              this.current_id = null;  // 保存新创建对话的ID
              window.location.reload();
              this.fetchThemes();
            })
            .catch(error => {
              console.error('Error:', error.message);
              alert('Failed to create and save conversation');
            });
      } else {
        // 如果当前ID不为null，更新已有对话
        fetch(`/api/conversations/update_conversation?id=`+this.current_id , {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
        })
            .then(response => {
              if (!response.ok) {
                throw new Error('Failed to update conversation');
              }
              return response.json();
            })
            .then(data => {
              alert('Conversation updated successfully.');
              this.messages_chatgpt = [];
              this.messages_tongyi = [];
              this.messages_wenxin = [];
              this.current_id=null;
              window.location.reload();
              this.fetchThemes();
            })
            .catch(error => {
              console.error('Error:', error.message);
              alert('Failed to update conversation');
            });
      }
    },
    renderMessage(message,sseMessage) {
      // 这里假设 this.md 是你的 markdown 渲染器
      if((this.current_id==null || this.flag) && sseMessage.zxakey=="zxa" ){
        return message;
      }
      return this.md.render(message);
    },


    deleteConversation(id) {
      axios.delete(`api/conversations/delete_conversation?id=`+id)
          .then(response => {
            console.log(response.data.message);
            // 如果需要，在这里可以更新界面上的数据或者进行其他操作
          })
          .catch(error => {
            console.error('Error deleting conversation:', error);
          });
      window.location.reload();
      this.fetchThemes();
    },

    async handleSearch() {
      // 如果正在加载中，则不执行新的搜索操作
      if (this.loading) {
        return;
      }
      this.flag=1;

      const keyword = this.queryKeyword;
      this.loading = true;
      try {
        let zxakey = "zxa";
        // 初始化一个用于 SSE 的 message 对象
        let wenxin_sseMessage = {
          orgcontent: '',
          content: '',
          role: 'assistant',
          zxakey: zxakey
        };
        let tongyi_sseMessage = {
          orgcontent: '',
          content: '',
          role: 'assistant',
          zxakey: zxakey
        };
        let chatgpt_sseMessage = {
          orgcontent: '',
          content: '',
          role: 'assistant',
          zxakey: zxakey
        };

        this.wenxin_messages.push({
          content: keyword,
          role: 'user'
        });
        this.tongyi_messages.push({
          content: keyword,
          role: 'user'
        });
        this.chatgpt_messages.push({
          content: keyword,
          role: 'user'
        });

        this.$nextTick(() => {
          this.scrollToBottom();
        });

        let wenxin_friendMessage = wenxin_sseMessage;
        this.wenxin_messages.push(wenxin_sseMessage);
        // 创建一个新的 EventSource 实例
        this.wenxin_eventSource = new EventSource('/api/wenxin?query=' + keyword,{ withCredentials: true });
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
              this.scrollToBottom();
            }
            //this.scrollToBottom();
          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        };

        this.queryKeyword = ''; // 清空输入框
        this.wenxin_eventSource.onerror = error => {
          console.error('EventSource failed:', error);
          this.wenxin_eventSource.close();
        };
        let tongyi_friendMessage = tongyi_sseMessage;
        this.tongyi_messages.push(tongyi_sseMessage);
        // 创建一个新的 EventSource 实例
        this.tongyi_eventSource = new EventSource('/api/tongyi?query=' + keyword,{ withCredentials: true });
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
              this.scrollToBottom();
            }
            //this.scrollToBottom();
          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        };
        this.queryKeyword = ''; // 清空输入框
        this.tongyi_eventSource.onerror = error => {
          console.error('EventSource failed:', error);
          this.tongyi_eventSource.close();
        };
        let chatgpt_friendMessage = chatgpt_sseMessage;
        this.chatgpt_messages.push(chatgpt_sseMessage);
        // 创建一个新的 EventSource 实例
        this.chatgpt_eventSource = new EventSource('/api/chatgpt?query=' + keyword,{ withCredentials: true });
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
              this.scrollToBottom();
            }

          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        };

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
      const messageContainer0 = this.$refs.messageContainer0;
      const messageContainer1 = this.$refs.messageContainer1;
      const messageContainer2 = this.$refs.messageContainer2;
      if (messageContainer0 && messageContainer1 && messageContainer2) {
        messageContainer0.scrollTop = messageContainer0.scrollHeight;
        messageContainer1.scrollTop = messageContainer1.scrollHeight;
        messageContainer2.scrollTop = messageContainer2.scrollHeight;
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
    },
    goToSetting(){
      router.push({ name: 'Setting'});
    },
    async handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file || !file.type.startsWith('image/')) {
        this.$message.error('请选择一张图片');
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        this.uploadedImages.push(e.target.result); // Base64 格式
        this.processImageWithModelAPI(e.target.result);
      };
      reader.readAsDataURL(file);
    },
    async processImageWithModelAPI(base64Image) {
      try {
        console.log("发送给后端的数据:", {
          image: base64Image
        });
        const response = await fetch('/api/vision', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            image: base64Image
          })
        });

        if (!response.ok) {
          throw new Error('图片分析失败');
        }
        const result = await response.json();
        this.parsedTextFromImage = result.text;
        this.queryKeyword += `\n【图片识别结果】:\n${result.text}`;
      } catch (error) {
        console.error('图片解析失败:', error);
        this.$message.error('图片解析失败，请重试');
      }
    },
  },
}
</script>

<style scoped>
/* 侧边栏样式 */
.sidebar {
  scrollbar-width: thin;
  scrollbar-color: #888 #f1f1f1;
}

.sidebar::-webkit-scrollbar {
  width: 6px;
}

.sidebar::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.sidebar::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: #555;
}

/* 消息容器样式 */
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

/* AI响应样式 */
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

/* 空状态样式 */
.empty-state {
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 24 24" fill="none" stroke="%23e5e7eb" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>');
  background-repeat: no-repeat;
  background-position: center;
  background-size: 30%;
  opacity: 0.5;
}

/* 聊天列悬停效果 */
.chat-column {
  transition: all 0.3s ease;
}

.chat-column:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* 覆盖Element UI样式 */
:deep(.el-input__inner) {
  height: 48px;
  border-radius: 12px;
  padding-right: 50px;
  border: 1px solid #e5e7eb;
}

:deep(.el-button) {
  border: none;
}

/* 按钮悬停效果 */
button:hover {
  transform: translateY(-1px);
}

/* 确保Font Awesome图标正常显示 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
</style>