# 猫头鹰工厂 (Owl Factory)

一个基于AI的智能视频内容分析平台，集成了GPU集群管理、任务调度、用户认证等功能。

## 项目概述

猫头鹰工厂是一个企业级的AI视频分析平台，提供以下核心功能：

- 🎥 **视频内容分析**: 支持多平台视频内容的智能分析
- 🖥️ **GPU集群管理**: 分布式GPU资源管理和任务调度
- 👥 **用户管理**: 完整的用户认证和权限管理系统
- 📊 **报告生成**: 自动生成详细的分析报告
- 💰 **充值系统**: 支持用户充值和消费管理
- 🔧 **API集成**: 集成MoreAPI等第三方服务

## 技术栈

### 前端
- React + TypeScript
- Vite 构建工具
- Tailwind CSS
- Framer Motion (动画)
- Lucide React (图标)

### 后端
- Python + FastAPI
- Supabase (数据库)
- JWT 认证
- Uvicorn (ASGI服务器)

### GPU集群
- Python 分布式计算
- SSH 远程管理
- Whisper 语音识别
- 负载均衡

## 项目结构

```
猫头鹰工场/
├── 前端页面/                 # React前端应用
│   ├── src/
│   │   ├── pages/            # 页面组件
│   │   ├── components/       # 通用组件
│   │   └── store/           # 状态管理
│   └── package.json
├── 后端程序/                 # FastAPI后端服务
│   ├── api/                 # API路由
│   ├── services/            # 业务逻辑
│   ├── models/              # 数据模型
│   └── requirements.txt
├── GPU服务器配置/            # GPU集群管理
│   ├── gpu_dashboard.py     # GPU监控面板
│   ├── cluster_manager.py   # 集群管理器
│   └── deployment_tools/    # 部署工具
├── 核心代码/                # 核心业务逻辑
├── 核心服务/                # 主要服务模块
├── 配置文件/                # 配置管理
└── 项目文档/                # 文档和说明
```

## 快速开始

### 环境要求
- Node.js 18+
- Python 3.10+
- GPU服务器 (可选)

### 安装依赖

#### 前端
```bash
cd 前端页面
npm install
npm run dev
```

#### 后端
```bash
cd 后端程序
pip install -r requirements.txt
python main.py
```

### 配置环境变量

1. 复制 `.env.example` 到 `.env`
2. 配置 Supabase 连接信息
3. 配置 JWT 密钥
4. 配置 GPU 服务器信息

## 主要功能模块

### 1. 用户管理
- 用户注册/登录
- JWT 令牌认证
- 权限控制
- 密码加密

### 2. 任务管理
- 任务创建和调度
- 状态跟踪
- 结果管理
- 错误处理

### 3. GPU集群
- 服务器监控
- 负载均衡
- 自动故障转移
- 性能统计

### 4. 报告系统
- 自动报告生成
- 多格式导出
- 历史记录
- 数据可视化

## API文档

### 认证接口
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `POST /auth/refresh` - 刷新令牌

### 任务接口
- `POST /tasks` - 创建任务
- `GET /tasks` - 获取任务列表
- `GET /tasks/{id}` - 获取任务详情
- `DELETE /tasks/{id}` - 删除任务

### GPU管理接口
- `GET /gpu/servers` - 获取GPU服务器列表
- `GET /gpu/status` - 获取集群状态
- `POST /gpu/deploy` - 部署任务到GPU

## 部署说明

### 开发环境
1. 启动后端服务: `python main.py`
2. 启动前端服务: `npm run dev`
3. 访问 `http://localhost:3000`

### 生产环境
1. 构建前端: `npm run build`
2. 配置 Nginx 反向代理
3. 使用 Gunicorn 部署后端
4. 配置 SSL 证书

## 监控和日志

- 应用日志: `logs/` 目录
- GPU监控: GPU Dashboard
- 性能指标: 内置监控面板
- 错误追踪: 集成错误报告

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 许可证

MIT License

## 联系方式

- 项目维护者: ft54482
- 邮箱: 48747218@qq.com

## 更新日志

### v1.0.0 (2024-12-29)
- 初始版本发布
- 基础功能实现
- GPU集群支持
- 用户认证系统