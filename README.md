# 🦉 猫头鹰工厂 (Owl Factory)

一个基于AI的智能视频内容分析平台，支持多平台视频内容的智能分析和洞察生成。

## 📋 项目概述

猫头鹰工厂是一个企业级的AI驱动视频分析平台，提供以下核心功能：

- 🎥 **单视频分析**：快速分析单个视频的语音转录和内容洞察
- 👥 **完整账号分析**：深度分析账号所有视频，生成综合报告
- 🔧 **GPU集群管理**：分布式GPU资源调度和监控
- 📊 **智能报告生成**：基于AI的内容分析和数据可视化
- 🛡️ **用户权限管理**：完整的用户认证和权限控制系统

## 🏗️ 技术架构

### 前端技术栈
- **React 18** + **TypeScript**
- **Vite** - 快速构建工具
- **Tailwind CSS** - 现代化样式框架
- **Framer Motion** - 动画库
- **React Router** - 路由管理
- **Zustand** - 状态管理
- **Radix UI** - 无障碍UI组件
- **Lucide React** - 图标库

### 后端技术栈
- **FastAPI** - 高性能异步API框架
- **Supabase** - 后端即服务平台
- **PostgreSQL** - 主数据库
- **Redis** - 缓存和会话存储
- **SQLAlchemy** - ORM框架
- **Loguru** - 日志管理
- **Pydantic** - 数据验证

### AI/ML技术栈
- **GPU集群** - 分布式计算资源
- **语音识别** - 视频转录服务
- **自然语言处理** - 内容分析
- **智能工作流** - 自动化分析流程

## 📁 项目结构

```
owl-factory/
├── frontend/                 # 前端应用
│   ├── src/
│   │   ├── components/      # React组件
│   │   │   ├── Layout.tsx           # 主布局组件
│   │   │   ├── ProtectedRoute.tsx   # 路由保护
│   │   │   ├── SuperAdminRoute.tsx  # 管理员路由
│   │   │   ├── AnalysisButtons.tsx  # 分析按钮组件
│   │   │   └── DataInputCard.tsx    # 数据输入卡片
│   │   ├── pages/           # 页面组件
│   │   ├── contexts/        # React上下文
│   │   ├── services/        # API服务
│   │   ├── store/           # 状态管理
│   │   └── App.tsx          # 主应用组件
│   ├── package.json         # 前端依赖配置
│   └── vite.config.ts       # Vite配置
├── backend/                  # 后端应用
│   ├── api/                 # API路由
│   │   └── intelligent_analysis_api.py  # 智能分析API
│   ├── config/              # 配置文件
│   ├── services/            # 业务服务
│   ├── models/              # 数据模型
│   ├── middleware/          # 中间件
│   ├── main.py              # 主应用入口
│   └── requirements.txt     # 后端依赖
└── README.md                # 项目说明文档
```

## 🚀 快速开始

### 环境要求

- Node.js >= 18.0.0
- Python >= 3.9
- PostgreSQL >= 13
- Redis >= 6.0

### 前端安装和运行

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### 后端安装和运行

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python main.py
```

### 环境配置

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 配置必要的环境变量：
```env
# Supabase配置
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/owl_factory

# Redis配置
REDIS_URL=redis://localhost:6379

# JWT配置
JWT_SECRET_KEY=your_jwt_secret_key
```

## 🎯 核心功能

### 1. 智能视频分析

- **单视频分析**：上传视频链接，快速获取内容转录和分析报告
- **批量分析**：支持多个视频同时分析
- **多平台支持**：抖音、小红书、B站、TikTok等主流平台

### 2. 账号深度分析

- **完整账号扫描**：分析账号所有公开视频
- **内容主题识别**：自动识别内容类型和主题
- **数据可视化**：生成详细的分析图表和报告

### 3. GPU集群管理

- **资源监控**：实时监控GPU使用情况
- **任务调度**：智能分配计算资源
- **性能优化**：自动优化分析流程

### 4. 用户管理系统

- **多级权限**：普通用户、管理员、超级管理员
- **安全认证**：基于JWT的安全认证机制
- **操作审计**：完整的用户操作日志

## 📊 API文档

### 智能分析API端点

- `POST /api/analysis/single-video` - 单视频分析
- `POST /api/analysis/complete-account` - 完整账号分析
- `GET /api/analysis/status/{task_id}` - 获取任务状态
- `GET /api/analysis/result/{task_id}` - 获取分析结果

### 用户管理API端点

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/users/profile` - 获取用户信息
- `PUT /api/users/profile` - 更新用户信息

### 管理员API端点

- `GET /api/admin/users` - 用户列表管理
- `GET /api/admin/gpu` - GPU资源管理
- `GET /api/admin/logs` - 系统日志查看

## 🔧 开发指南

### 代码规范

- 前端使用ESLint + Prettier进行代码格式化
- 后端遵循PEP 8 Python代码规范
- 使用TypeScript进行类型检查
- 提交前运行测试用例

### 贡献指南

1. Fork项目仓库
2. 创建功能分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 创建Pull Request

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- ✨ 初始版本发布
- 🎥 单视频分析功能
- 👥 完整账号分析功能
- 🔧 GPU集群管理
- 🛡️ 用户权限系统
- 📊 智能报告生成

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 支持与联系

- 📧 邮箱：support@owl-factory.com
- 🐛 问题反馈：[GitHub Issues](https://github.com/ft54482/owl-factory/issues)
- 📖 文档：[项目文档](https://docs.owl-factory.com)

---

**猫头鹰工厂** - 让AI为您的视频内容分析赋能 🦉✨