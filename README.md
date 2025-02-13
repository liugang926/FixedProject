# 资产管理系统

基于 Vue 3 + Django 的固定资产管理系统。

## 技术栈

### 前端
- Vue 3
- Vue Router
- Vuex
- Element Plus
- Axios
- SCSS

### 后端
- Django
- Django REST framework
- MySQL
- JWT认证

## 已实现功能

### 用户管理
- [x] 用户登录/退出
- [x] 个人中心
  - 基本信息修改
  - 密码修改
- [x] 用户管理（管理员）
- [x] 角色管理（管理员）
- [x] 权限管理（管理员）

### 系统功能
- [x] 动态路由和权限控制
- [x] 页面刷新保持状态
- [x] 响应式布局
- [x] Token 认证

## 待实现功能

### 1. 资产基础管理
- [ ] 资产分类管理
- [ ] 资产编码规则设置
- [ ] 资产状态管理（在用、闲置、报废等）

### 2. 资产操作管理
- [ ] 资产入库
- [ ] 资产领用
- [ ] 资产归还
- [ ] 资产调拨
- [ ] 资产维修
- [ ] 资产报废

### 3. 资产信息管理
- [ ] 资产基本信息
- [ ] 资产详细信息
- [ ] 资产附件管理
- [ ] 资产图片管理
- [ ] 资产变更记录

### 4. 资产查询统计
- [ ] 资产查询
- [ ] 资产统计
- [ ] 资产报表导出
- [ ] 资产盘点管理

### 5. 资产预警管理
- [ ] 保修期预警
- [ ] 使用年限预警
- [ ] 维保到期预警
- [ ] 库存预警

### 6. 资产财务管理
- [ ] 资产价值管理
- [ ] 折旧管理
- [ ] 维修成本统计
- [ ] 资产总值统计

### 7. 审批流程管理
- [ ] 资产申请审批
- [ ] 资产调拨审批
- [ ] 资产报废审批
- [ ] 审批流程配置

### 8. 系统配置
- [ ] 部门管理
- [ ] 存放地点管理
- [ ] 供应商管理
- [ ] 品牌管理

### 9. 数据导入导出
- [ ] 资产数据导入
- [ ] 资产数据导出
- [ ] 历史数据迁移
- [ ] 数据备份恢复

### 10. 移动端功能
- [ ] 移动端资产扫码
- [ ] 移动端资产查询
- [ ] 移动端资产盘点
- [ ] 移动端审批处理

## API 接口

### 用户相关
```
POST /api/auth/login/ - 用户登录
POST /api/users/logout/ - 用户登出
GET /api/users/me/ - 获取当前用户信息
PUT /api/users/profile/ - 更新用户信息
POST /api/users/{id}/change_password/ - 修改用户密码
```

## 开发说明

### 前端开发
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run serve

# 构建生产版本
npm run build
```

### 后端开发
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移
python manage.py migrate

# 启动开发服务器
python manage.py runserver
```

## 注意事项

1. 权限控制
   - 基于角色的访问控制（RBAC）
   - 动态路由权限
   - API接口权限

2. 数据安全
   - Token认证
   - 密码加密
   - 敏感数据保护

3. 性能优化
   - 路由懒加载
   - 组件按需加载
   - 数据缓存处理

## 开发计划

1. 第一阶段：基础功能
   - [x] 用户认证
   - [x] 权限管理
   - [ ] 资产基础管理

2. 第二阶段：核心功能
   - [ ] 资产操作管理
   - [ ] 资产信息管理
   - [ ] 资产查询统计

3. 第三阶段：高级功能
   - [ ] 资产预警管理
   - [ ] 资产财务管理
   - [ ] 审批流程管理

4. 第四阶段：扩展功能
   - [ ] 系统配置完善
   - [ ] 数据导入导出
   - [ ] 移动端适配

## 技术要点

1. 前端
   - Vue 3 组合式 API
   - Vuex 状态管理
   - 动态路由
   - 权限控制
   - UI组件封装

2. 后端
   - Django REST framework
   - JWT认证
   - 数据库设计
   - 接口安全
   - 性能优化

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 发起 Pull Request

## 许可证

[MIT](LICENSE)

## 项目结构

```
asset-management/
├── backend/                    # 后端项目目录
│   ├── apps/                  # Django 应用目录
│   │   ├── assets/           # 资产管理应用
│   │   │   ├── migrations/   # 数据库迁移文件
│   │   │   ├── models.py     # 资产相关模型
│   │   │   ├── serializers.py # 序列化器
│   │   │   ├── urls.py       # URL 配置
│   │   │   └── views.py      # 视图函数
│   │   └── users/            # 用户管理应用
│   │       ├── migrations/   
│   │       ├── models.py     # 用户模型
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       └── views.py
│   ├── config/                # 项目配置目录
│   │   ├── settings/         # 设置文件
│   │   │   ├── base.py      # 基础配置
│   │   │   ├── dev.py       # 开发环境配置
│   │   │   └── prod.py      # 生产环境配置
│   │   ├── urls.py          # 主 URL 配置
│   │   └── wsgi.py          # WSGI 配置
│   ├── utils/                # 工具函数目录
│   │   ├── auth.py          # 认证相关
│   │   └── permissions.py    # 权限相关
│   ├── manage.py            # Django 管理脚本
│   └── requirements.txt     # Python 依赖
│
├── frontend/                  # 前端项目目录
│   ├── public/              # 静态资源
│   │   ├── favicon.ico
│   │   └── index.html
│   ├── src/                 # 源代码目录
│   │   ├── api/            # API 接口
│   │   │   ├── asset.js
│   │   │   └── user.js
│   │   ├── assets/         # 资源文件
│   │   │   ├── icons/
│   │   │   └── styles/
│   │   ├── components/     # 公共组件
│   │   │   ├── Breadcrumb/
│   │   │   ├── Hamburger/
│   │   │   └── SvgIcon/
│   │   ├── layout/         # 布局组件
│   │   │   ├── components/
│   │   │   └── index.vue
│   │   ├── router/         # 路由配置
│   │   │   └── index.js
│   │   ├── store/          # Vuex 状态管理
│   │   │   ├── modules/
│   │   │   └── index.js
│   │   ├── styles/         # 样式文件
│   │   │   ├── element-ui.scss
│   │   │   ├── index.scss
│   │   │   ├── mixin.scss
│   │   │   ├── sidebar.scss
│   │   │   ├── transition.scss
│   │   │   └── variables.scss
│   │   ├── utils/          # 工具函数
│   │   │   ├── auth.js
│   │   │   ├── request.js
│   │   │   └── validate.js
│   │   ├── views/          # 页面组件
│   │   │   ├── assets/
│   │   │   ├── dashboard/
│   │   │   ├── login/
│   │   │   └── profile/
│   │   ├── App.vue         # 根组件
│   │   ├── main.js         # 入口文件
│   │   └── permission.js   # 权限控制
│   ├── .env.development    # 开发环境变量
│   ├── .env.production     # 生产环境变量
│   ├── package.json        # 项目依赖
│   └── vue.config.js       # Vue 配置
│
├── .gitignore              # Git 忽略文件
├── LICENSE                 # 许可证文件
└── README.md              # 项目说明文档
```