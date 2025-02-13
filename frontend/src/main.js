import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/styles/main.scss'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import permission from './directives/permission'

const app = createApp(App)

// 注册 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 注册权限指令
app.directive('permission', permission)

app.use(store)
   .use(router)
   .use(ElementPlus)
   .mount('#app') 