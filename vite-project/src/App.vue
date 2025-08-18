<script setup>
import { ref } from 'vue'
import { ElContainer, ElHeader, ElAside, ElMain, ElFooter, ElScrollbar, ElMenu, ElSubMenu, ElMenuItem, ElMenuItemGroup, ElIcon, ElRow, ElCol, ElButton, ElCard, ElMessage, ElInput } from 'element-plus'
import {
  Message,     // 消息图标
  Menu as IconMenu, // 菜单图标(重命名避免冲突)
  Setting,     // 设置图标
  Check,
  Delete,
  Edit,
  Search,
  Star,
} from '@element-plus/icons-vue'

// 优化：使用正确的公共资源路径
const getImagePath = (name) => {
  return `/static/images/${name}`
}

// 定义卡片数据
const cards = ref([
  // 运维工具组
  {
    group: "运维工具",
    items: [
      { title: '堡垒机', icon: getImagePath('堡垒机.png'), link: 'https://192.168.0.98' },
      { title: 'VPN', icon: getImagePath('vpn.png'), link: 'https://sslvpn.yofoto.cn:4433' },
      { title: '超融合', icon: getImagePath('超融合.png'), link: 'http://192.168.5.10:5000' },
      { title: 'zupu-jenkins', icon: getImagePath('jenkins.ico'), link: 'http://192.168.7.116:8080' },
      { title: 'xxl-job', icon: getImagePath('xxl-job.png'), link: 'http://14.103.92.53:8090/xxl-job-admin' },
      { title: 'nacos', icon: getImagePath('nacos.png'), link: 'http://14.103.92.53:8848/nacos' },
      { title: '火山云', icon: getImagePath('火山引擎.png'), link: 'https://www.volcengine.com/' },
      { title: 'test-esxi', icon: getImagePath('esxi.svg'), link: 'https://192.168.4.110' },
      { title: 'zupu-esxi', icon: getImagePath('esxi.svg'), link: 'https://192.168.29.110' },
      { title: 'ESXI-70', icon: getImagePath('esxi.svg'), link: 'https://192.168.31.70' },
      { title: 'ESXI-71', icon: getImagePath('esxi.svg'), link: 'https://192.168.31.71' },
      { title: 'zupu-neo4j', icon: getImagePath('neo4j.ico'), link: 'http://14.103.92.53:7474' },
      { title: 'zupu-kibana', icon: getImagePath('kibana.png'), link: 'http://14.103.92.53:5601' },
      { title: 'gitlab', icon: getImagePath('gitlab.png'), link: 'https://gitlab.yofoto.cn' },
    ]
  }, 
  {
    group: "监控",
    items: [
      { title: '夜莺', icon: getImagePath('夜莺.png'), link: 'http://192.168.0.63:17000' },
      { title: '内网-Prom', icon: getImagePath('prometheus.png'), link: 'http://192.168.7.76:9090' },
      { title: 'zupu-Prom', icon: getImagePath('prometheus.png'), link: 'http://14.103.92.53:9090' },
      { title: '夜莺-Prom', icon: getImagePath('prometheus.png'), link: 'http://192.168.0.63:9090' },
      { title: 'yihai-Prom', icon: getImagePath('prometheus.png'), link: 'http://14.103.162.150:9090' },
      { title: '派享云-Prom', icon: getImagePath('prometheus.png'), link: 'http://14.103.162.150:9090' },
      { title: '蜂鸟部落-Prom', icon: getImagePath('prometheus.png'), link: 'http://14.103.92.163:9090' },
      { title: '网络-Prom', icon: getImagePath('prometheus.png'), link: 'http://192.168.7.187:9090' },
      { title: '内网-grafana', icon: getImagePath('grafana.png'), link: 'http://192.168.7.76:3000' },
      { title: 'zupu-grafana', icon: getImagePath('grafana.png'), link: 'http://14.103.92.53:3000' },
      { title: '夜莺-grafana', icon: getImagePath('grafana.png'), link: 'http://192.168.0.63:3000' },
      { title: '网络-grafana', icon: getImagePath('grafana.png'), link: 'http://192.168.7.187:3000' },
    ]
  },
  {
    group: "工具",
    items: [
      { title: '密码工具', icon: getImagePath('密码.png'), link: 'https://mima.yofoto.com' },
      { title: 'closeai', icon: getImagePath('closeai.png'), link: 'https://www.closeai-asia.com' },
      { title: 'dootask', icon: getImagePath('dootask.png'), link: 'http://dootask.yofoto.cn/' },
      { title: 'oa', icon: getImagePath('oa.png'), link: 'https://oa.yofoto.cn/' },
      { title: '邮箱', icon: getImagePath('邮箱.png'), link: 'https://mail.yofoto.cn/' },
      { title: 'nginx-web', icon: getImagePath('nginx-web.ico'), link: 'http://192.168.4.50:8000' },
    ]
  },
  {
    group: "文档",
    items: []
  }
])

// 搜索相关数据和方法
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)

const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }

  isSearching.value = true
  try {
    // 调用后端搜索API
    const response = await fetch(`http://localhost:5000/search?q=${encodeURIComponent(searchQuery.value)}`)
    const data = await response.json()
    searchResults.value = data.results
  } catch (error) {
    console.error('搜索失败:', error)
    ElMessage.error('搜索失败，请稍后重试')
  } finally {
    isSearching.value = false
  }
}

// 统一跳转处理方法
const handleCardClick = (url) => {
  window.open(url, '_blank', 'noopener,noreferrer')
}
const handleMenuClick = (url) => {
  window.open(url, '_blank', 'noopener,noreferrer')
}

// 锚点跳转方法 - 修改为接受分组ID
const scrollToGroup = (groupId) => {
  const target = document.getElementById(`group-${groupId}`)
  if (target) {
    // 计算偏移量：顶部导航栏高度 + 20px
    const offset = 60 + 20
    const targetPosition = target.offsetTop - offset
    
    // 获取卡片容器元素
    const cardContainer = document.querySelector('.card-container')
    if (cardContainer) {
      cardContainer.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      })
    }
  }
}
</script>

<template>
  <el-container style="height: 100vh" class="main-container">
    <el-header style="background:rgb(127, 179, 231); color: white" class="custom-header">
      <div style="display: flex; justify-content: space-between; align-items: center; width: 100%">
        <h1>自用导航页面</h1>
        <div class="search-container">
          <el-input
            v-model="searchQuery"
            placeholder="搜索..."
            prefix-icon="Search"
            @icon-click="handleSearch"
            style="width: 200px;"/>
        </div>
      </div>
    </el-header>
    <el-container class="content-wrapper">
      <!-- 搜索结果区域 -->
      <div v-if="searchResults.length > 0" class="search-results">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>搜索结果 ({{ searchResults.length }})</span>
            </div>
          </template>
          <div class="search-result-list">
            <div v-for="result in searchResults" :key="result.id" class="search-result-item" @click="handleCardClick(result.link)">
              <img :src="result.icon" alt="{{ result.title }}" class="result-icon">
              <div class="result-info">
                <h3 class="result-title">{{ result.title }}</h3>
                <p class="result-group">{{ result.group }}</p>
                <p class="result-link">{{ result.link }}</p>
              </div>
            </div>
          </div>
        </el-card>
      </div>
      <!-- 主侧边栏 -->
      <el-aside width="200px">
        <el-scrollbar>
          <el-menu :default-openeds="['1', '3']">
            <el-sub-menu index="2">
              <template #title>
                <el-icon><icon-menu /></el-icon>菜单
              </template>
              <!-- 添加点击事件，滚动到对应分组 -->
              <el-menu-item index="2-1" @click="scrollToGroup(0)">运维工具</el-menu-item>
              <el-menu-item index="2-2" @click="scrollToGroup(1)">监控</el-menu-item>
              <el-menu-item index="2-3" @click="scrollToGroup(2)">工具</el-menu-item>
              <el-menu-item index="2-4" @click="handleMenuClick('http://192.168.4.50:5010')">文档</el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-scrollbar>
      </el-aside>

      <!-- 主页 -->
      <el-main style="padding: 0; overflow: hidden;">
        <div class="card-container">
          <!-- 按组渲染卡片 -->
          <!-- 为每个组容器添加唯一ID -->
          <div v-for="(group, groupIndex) in cards" :key="groupIndex" 
               :id="`group-${groupIndex}`" 
               class="group-container">
            <!-- 组标题 -->
            <h2 class="group-title">{{ group.group }}</h2>
            
            <!-- 每组卡片内容 -->
            <div v-for="(row, rowIndex) in Math.ceil(group.items.length / 5)" 
                :key="rowIndex"
                class="card-row">
              <el-card
                v-for="(card, cardIndex) in group.items.slice(rowIndex * 5, (rowIndex + 1) * 5)"
                :key="cardIndex"
                class="card-item"
                @click="handleCardClick(card.link)"
              >
                <div class="card-content">
                  <img :src="card.icon" class="card-icon" v-if="card.icon">
                  <span class="card-title">{{ card.title }}</span>
                </div>
              </el-card>
            </div>
          </div>
        </div>
      </el-main>
    </el-container>
    <el-footer style="background:rgb(59, 62, 70); color: white">Footer</el-footer>
  </el-container>
</template>

<style scoped>

/* 卡片容器样式 */
.card-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
  padding: 16px;
  height: calc(100vh - 120px);
  overflow-y: auto;
  scroll-behavior: smooth; /* 添加平滑滚动效果 */
}

/* 组容器样式 */
.group-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
  /* 为锚点跳转添加过渡效果 */
  transition: transform 0.3s ease;
}

/* 添加锚点跳转时的视觉效果 */
.group-container:target {
  animation: highlight 1.5s ease;
}

@keyframes highlight {
  0% {
    background-color: rgba(127, 179, 231, 0.1);
  }
  100% {
    background-color: transparent;
  }
}
</style>
<style scoped>
/* 消除默认边距 */
.main-container {
  height: 100vh;
  margin: 0;
  padding: 0;
}
.custom-header {
  background: rgb(127, 179, 231);
  color: white;
  border-bottom: 1px solid #ddd;
  padding: 0 20px !important; /* 覆盖element默认padding */
  display: flex;
  align-items: center;
}

/* 确保 el-main 宽度正确 */
.content-wrapper {
  display: flex;
  flex: 1;
  overflow: hidden;
}


/* 组标题样式 */
.group-title {
  margin: 0 0 15px 15px;
  font-size: 22px;
  color: #333;
  font-weight: bold;
  padding-bottom: 8px;
  border-bottom: 2px solid rgb(127, 179, 231);
}

.card-row {
  display: flex;
  gap: 50px;  /* 列间距控制 */
  width: 100%;
  min-height: 65px;
  min-width: 280px;
  flex-wrap: wrap; /* 确保在小屏幕自动换行 */
}
.card-item {
  width: 280px !important; /* 固定宽度 */
  height: 65px;
  flex-shrink: 0; /* 禁止压缩 */
  position: relative; /* 为序号标签定位 */
  cursor: pointer; /* 鼠标悬停指针效果 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 添加过渡效果 */
}
.card-item:hover {
  transform: translateY(-3px); /* 悬停上浮效果 */
  box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* 添加阴影效果 */
}
.card-content {
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 0 15px;
}

.card-icon {
  width: 35px;
  height: 35px; /* 建议统一尺寸 */
  object-fit: contain;
  flex-shrink: 0;
}
.card-title {
  margin-left: 40px;
  font-size: 20px;
  letter-spacing: 1px;
  color: rgb(199, 30, 100);
  display: flex;
  transform: translateY(-5px);/* 修改卡片内上下距离 */
  align-items: center; /* 确保文字垂直居中 */
  height: 100%; /* 确保高度100% */
}

/* 搜索结果样式 */
.search-results {
  padding: 16px;
  width: 100%;
}

.search-result-list {
  margin-top: 10px;
}

.search-result-item {
  display: flex;
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-result-item:hover {
  background-color: #f5f7fa;
}

.result-icon {
  width: 35px;
  height: 35px;
  object-fit: contain;
  flex-shrink: 0;
}

.result-info {
  margin-left: 16px;
  flex-grow: 1;
}

.result-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #333;
}

.result-group {
  font-size: 12px;
  color: #666;
  margin: 4px 0;
}

.result-link {
  font-size: 12px;
  color: #1890ff;
  margin: 0;
  word-break: break-all;
}
</style>
<style>
/* 全局覆盖element样式 */
:deep(.el-card__body) {
  padding: 0 !important;
  width: 100%;
  height: 100%;
}

/* 组标题悬停效果 */
.group-title:hover {
  color: rgb(199, 30, 100);
  transition: color 0.3s;
}
</style>