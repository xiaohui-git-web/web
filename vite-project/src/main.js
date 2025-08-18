import { createApp } from 'vue'
import App from './App.vue'
import './ma.css'
// 导入ElementPlus组件
import { ElContainer, ElHeader, ElAside, ElMain, ElFooter ,ElCol,} from 'element-plus'

// 导入ElementPlus样式
import '/data/xm/vite-project/node_modules/element-plus/dist/index.css'

const app = createApp(App)
app.use(ElContainer)
app.use(ElHeader)
app.use(ElAside)
app.use(ElMain)
app.use(ElFooter)
app.use(ElCol)
      // 使用ElementPlus组件
createApp(App).mount('#app')

