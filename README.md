# 资产管理系统

一个基于 Django + Vue.js 的资产管理系统，用于管理企业资产的分配、转移和跟踪。

## 开发环境部署

### 系统要求
- Python 3.8+
- Node.js 14+
- npm 6+ 或 yarn 1.22+

### 后端部署

1. 创建并激活虚拟环境
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

2. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

3. 初始化数据库
```bash
python manage.py makemigrations users
python manage.py makemigrations assets
python manage.py migrate

# 创建超级管理员账号
python manage.py createsuperuser
# 按提示输入：
# - 用户名
# - 邮箱（可选）
# - 密码（至少8位）
# - 确认密码
```

4. 运行开发服务器
```bash
python manage.py runserver
```

5. 访问管理后台
```
访问 http://localhost:8000/admin
使用刚才创建的超级管理员账号登录
可以在这里管理：
- 用户账号
- 资产分类
- 资产信息
- 资产转移记录
```

### 前端部署

1. 安装依赖
```bash
cd frontend
npm install
# 或者使用 yarn
yarn install
```

2. 运行开发服务器
```bash
npm run serve
# 或者使用 yarn
yarn serve
```

### 开发注意事项

1. 数据库迁移
- 修改模型后需要执行迁移命令
- 如果遇到迁移问题，可以尝试删除所有迁移文件并重新生成：
```bash
# Windows
Remove-Item -Path "assets/migrations/0*.py" -Force
Remove-Item -Path "users/migrations/0*.py" -Force

# Linux/MacOS
rm assets/migrations/0*.py
rm users/migrations/0*.py
```

2. 环境变量
- 开发环境可以使用 .env 文件配置环境变量
- 不要将包含敏感信息的 .env 文件提交到版本控制

3. API 文档
- API 文档可以通过访问 http://localhost:8000/api/docs/ 查看
- 确保安装了 drf-yasg 包以支持 Swagger 文档

4. 模型引用规范
- 所有模型文件应放在对应的应用目录下
- 不要在 backend/models/ 目录下创建重复的模型文件
- 在服务层引用模型时使用正确的导入路径
- 在服务层代码中使用 get_user_model() 获取用户模型：
```python
# 正确的引用方式
from assets.models import Asset, AssetCategory
from django.contrib.auth import get_user_model

User = get_user_model()

# 错误的引用方式
from django.contrib.auth.models import User  # 不要直接使用
from ..models.asset import Asset  # 不要使用重复的模型文件
```

### 常见问题

1. 用户模型关联问题
- 确保 settings.py 中的 AUTH_USER_MODEL 设置在文件最开始
- 在模型中使用字符串引用 'users.User' 而不是 settings.AUTH_USER_MODEL
- 如果遇到用户模型关联问题，按以下步骤处理：
  1. 确保 settings.py 中 AUTH_USER_MODEL = 'users.User' 在所有导入之前
  2. 在 INSTALLED_APPS 中确保 users 应用在 django.contrib.auth 之前
  3. 在其他应用中引用用户模型时使用字符串引用 'users.User'
  4. 清理所有迁移文件和 __pycache__ 后重新迁移
```bash
# 清理命令
Remove-Item -Path "assets/migrations/0*.py" -Force
Remove-Item -Path "users/migrations/0*.py" -Force
Get-ChildItem -Path . -Filter "__pycache__" -Recurse | Remove-Item -Force -Recurse

# 重新迁移
python manage.py makemigrations users
python manage.py makemigrations assets
python manage.py migrate
```

2. 跨域问题
- 检查 CORS 配置是否正确
- 确保 API 请求包含正确的 headers

3. 数据库迁移问题
- 如果遇到迁移冲突，尝试重新生成迁移文件
- 检查模型的外键关系是否正确

## 项目结构

固定资产管理系统/
├── backend/                    # 后端项目
│   ├── config/                 # 配置文件
│   ├── controllers/           # 控制器
│   ├── assets/               # 资产管理应用
│   │   ├── models.py        # 资产相关模型
│   │   └── tests.py        # 测试文件
│   ├── users/               # 用户管理应用
│   │   └── models.py       # 用户模型
│   ├── services/             # 业务逻辑
│   ├── utils/                # 工具类
│   └── requirements.txt      # Python依赖
│
├── frontend/                   # 前端项目 
│   ├── public/               # 静态资源
│   ├── src/                  # 源代码
│   │   ├── api/             # API接口
│   │   ├── components/      # 组件
│   │   ├── router/          # 路由配置
│   │   ├── store/           # 状态管理
│   │   ├── utils/           # 工具函数
│   │   └── views/           # 页面视图
│   └── package.json         # 依赖配置
│
└── docs/                      # 项目文档
    ├── api/                  # API文档
    ├── database/            # 数据库设计文档
    └── deployment/          # 部署文档
#   F i x e d P r o j e c t 
 
 