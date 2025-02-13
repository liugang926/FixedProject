import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layout/index.vue'

// 基础路由
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index.vue'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘', icon: 'Odometer', affix: true }
      }
    ]
  },
  {
    path: '/404',
    name: '404',
    component: () => import('@/views/error/404.vue'),
    hidden: true
  },
  {
    path: '/profile',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '',
        name: 'Profile',
        component: () => import('@/views/profile/index.vue'),
        meta: { title: '个人中心' }
      }
    ]
  }
]

// 需要根据权限动态加载的路由
export const asyncRoutes = [
  {
    path: '/system',
    component: Layout,
    redirect: '/system/user',
    alwaysShow: true,
    name: 'System',
    meta: { 
      title: '系统管理', 
      icon: 'Setting'
    },
    children: [
      {
        path: 'user',
        name: 'User',
        component: () => import('@/views/user/index.vue'),
        meta: { 
          title: '用户管理', 
          icon: 'User'
        }
      },
      {
        path: 'role',
        name: 'Role',
        component: () => import('@/views/role/index.vue'),
        meta: { 
          title: '角色管理', 
          icon: 'UserFilled'
        }
      },
      {
        path: 'permission',
        name: 'Permission',
        component: () => import('@/views/permission/index.vue'),
        meta: { 
          title: '权限管理', 
          icon: 'Lock'
        }
      }
    ]
  },
  {
    path: '/asset',
    component: Layout,
    redirect: '/asset/list',
    alwaysShow: true,
    name: 'Asset',
    meta: { 
      title: '资产管理', 
      icon: 'Files'
    },
    children: [
      {
        path: 'list',
        name: 'AssetList',
        component: () => import('@/views/assets/AssetList.vue'),
        meta: { 
          title: '资产列表', 
          icon: 'Document'
        }
      }
    ]
  }
]

// 所有路由
export const allRoutes = [...constantRoutes, ...asyncRoutes, {
  path: '/:pathMatch(.*)*',
  redirect: '/404',
  hidden: true
}]

const router = createRouter({
  history: createWebHistory(),
  routes: allRoutes // 直接使用所有路由
})

export function resetRouter() {
  const newRouter = createRouter({
    history: createWebHistory(),
    routes: allRoutes
  })
  router.matcher = newRouter.matcher
}

export default router 