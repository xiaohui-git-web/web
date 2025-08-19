import { createApp } from 'vue'
import App from './App.vue'
import './ma.css'
// 完整导入ElementPlus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)
      // 使用ElementPlus组件
app.mount('#app')

