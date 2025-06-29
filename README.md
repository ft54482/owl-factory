# 猫头鹰工厂 (Owl Factory)

一个专为AI智能视频分析平台，集成多平台视频解析、GPU集群管理、任务分发和智能分析功能。

## 🚀 项目概述

猫头鹰工厂是一个企业级的AI视频分析平台，提供以下核心功能：

- **视频解析分析**: 支持多平台视频内容的智能分析
- **GPU集群管理**: 分布式GPU资源调度和监控
- **用户管理**: 完整的用户认证和权限管理系统
- **数据生成**: 自动生成详细的分析报告

## 📁 项目结构

```
owl-factory/
├── backend/                 # 后端服务 (原: 后端程序)
│   ├── api/                # API路由模块
│   │   ├── admin_routes.py # 管理员路由
│   │   ├── auth_routes.py  # 认证路由
│   │   ├── gpu_routes.py   # GPU管理路由
│   │   ├── log_routes.py   # 日志路由
│   │   ├── recharge_routes.py # 充值路由
│   │   ├── user_routes.py  # 用户路由
│   │   └── intelligent_analysis_api.py # 智能分析API
│   ├── config/             # 配置模块
│   │   └── supabase_config.py # Supabase配置
│   ├── database/           # 数据库模块
│   ├── middleware/         # 中间件
│   ├── models/             # 数据模型
│   ├── services/           # 业务服务
│   ├── scripts/            # 脚本工具
│   ├── main.py            # 应用入口
│   ├── requirements.txt   # Python依赖
│   └── Dockerfile         # Docker配置
├── frontend/               # 前端应用 (原: 前端页面)
│   ├── src/               # 源代码
│   │   ├── components/    # React组件
│   │   ├── contexts/      # React上下文
│   │   ├── lib/          # 工具库
│   │   ├── pages/        # 页面组件
│   │   ├── services/     # API服务
│   │   ├── store/        # 状态管理
│   │   ├── types/        # TypeScript类型
│   │   ├── App.tsx       # 主应用组件
│   │   ├── main.tsx      # 应用入口
│   │   └── index.css     # 全局样式
│   ├── index.html        # HTML模板
│   ├── package.json      # Node.js依赖
│   ├── vite.config.ts    # Vite配置
│   ├── tailwind.config.js # Tailwind配置
│   ├── tsconfig.json     # TypeScript配置
│   └── Dockerfile        # Docker配置
├── gpu-cluster/           # GPU集群管理
├── nginx/                 # Nginx配置
├── config/               # 全局配置
├── logs/                 # 日志文件
├── reports/              # 分析报告
├── uploads/              # 上传文件
├── docker-compose.yml    # Docker编排
├── .env.example          # 环境变量模板
└── PROJECT_STRUCTURE.md  # 项目结构说明
```

## 🛠️ 技术栈

### 后端技术
- **Python 3.11+**: 主要开发语言
- **FastAPI**: 高性能Web框架
- **Supabase**: 数据库和认证服务
- **Redis**: 缓存和任务队列
- **Whisper**: 语音识别
- **PyTorch**: AI模型推理

### 前端技术
- **React 18**: 用户界面框架
- **TypeScript**: 类型安全的JavaScript
- **Vite**: 现代化构建工具
- **Tailwind CSS**: 实用优先的CSS框架
- **Zustand**: 轻量级状态管理

### 基础设施
- **Docker**: 容器化部署
- **Nginx**: 反向代理和负载均衡
- **Prometheus**: 监控指标收集
- **Grafana**: 监控面板
- **Logstash**: 日志收集

## 🚀 快速开始

### 环境要求

- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+ (开发环境)
- Python 3.11+ (开发环境)

### 1. 克隆项目

```bash
git clone https://github.com/ft54482/owl-factory.git
cd owl-factory
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量文件
nano .env
```

**重要配置项：**
- `SUPABASE_URL`: Supabase项目URL
- `SUPABASE_ANON_KEY`: Supabase匿名密钥
- `SUPABASE_SERVICE_ROLE_KEY`: Supabase服务角色密钥
- `JWT_SECRET_KEY`: JWT签名密钥
- `GPU_SERVERS`: GPU服务器配置

### 3. 启动服务

```bash
# 使用Docker Compose启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 4. 访问应用

- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **监控面板**: http://localhost:3001 (Grafana)
- **指标收集**: http://localhost:9090 (Prometheus)

## 🔧 开发环境设置

### 后端开发

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📊 核心功能

### 1. 智能视频分析

- **单视频分析**: 上传视频文件进行AI分析
- **账号完整分析**: 分析整个社交媒体账号的内容
- **多平台支持**: 抖音、小红书、B站、TikTok等
- **实时处理**: GPU集群加速的实时分析

### 2. GPU集群管理

- **资源监控**: 实时监控GPU使用率和状态
- **任务调度**: 智能分配计算任务到可用GPU
- **负载均衡**: 自动平衡集群负载
- **故障恢复**: 自动检测和恢复故障节点

### 3. 用户管理系统

- **用户注册/登录**: 完整的认证流程
- **权限管理**: 基于角色的访问控制
- **充值系统**: 用户余额和消费管理
- **使用统计**: 详细的使用记录和统计

### 4. 数据分析报告

- **自动生成**: AI自动生成分析报告
- **多格式导出**: PDF、Excel、JSON等格式
- **可视化图表**: 丰富的数据可视化
- **历史记录**: 完整的分析历史追踪

## 🔐 安全特性

- **JWT认证**: 安全的用户认证机制
- **CORS保护**: 跨域请求安全控制
- **速率限制**: API请求频率限制
- **数据加密**: 敏感数据加密存储
- **SSL/TLS**: HTTPS安全传输

## 📈 监控和日志

- **应用监控**: Prometheus + Grafana监控面板
- **日志收集**: 集中化日志收集和分析
- **性能指标**: 详细的性能监控指标
- **告警系统**: 自动故障检测和告警

## 🚀 部署指南

### 生产环境部署

1. **服务器要求**:
   - CPU: 8核心以上
   - 内存: 16GB以上
   - 存储: 500GB以上SSD
   - GPU: NVIDIA GPU (可选，用于AI加速)

2. **域名配置**:
   ```bash
   # 配置域名解析
   api.yourdomain.com -> 服务器IP
   app.yourdomain.com -> 服务器IP
   ```

3. **SSL证书**:
   ```bash
   # 使用Let's Encrypt获取免费SSL证书
   certbot --nginx -d api.yourdomain.com -d app.yourdomain.com
   ```

4. **环境变量配置**:
   ```bash
   # 生产环境配置
   ENVIRONMENT=production
   DEBUG=false
   DOMAIN=yourdomain.com
   SSL_ENABLED=true
   ```

### Docker部署

```bash
# 构建并启动所有服务
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# 扩展工作进程
docker-compose up -d --scale task-worker=4

# 更新服务
docker-compose pull
docker-compose up -d
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 API文档

详细的API文档可以在运行服务后访问：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 主要API端点

- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `POST /api/analysis/video` - 单视频分析
- `POST /api/analysis/account` - 账号完整分析
- `GET /api/gpu/status` - GPU集群状态
- `GET /api/reports/{report_id}` - 获取分析报告

## 🐛 故障排除

### 常见问题

1. **Docker服务启动失败**
   ```bash
   # 检查日志
   docker-compose logs service_name
   
   # 重启服务
   docker-compose restart service_name
   ```

2. **数据库连接失败**
   - 检查Supabase配置
   - 验证网络连接
   - 确认环境变量设置

3. **GPU不可用**
   - 检查NVIDIA驱动
   - 验证CUDA安装
   - 确认Docker GPU支持

4. **前端构建失败**
   ```bash
   # 清理缓存
   npm cache clean --force
   rm -rf node_modules
   npm install
   ```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系我们

- **项目维护者**: ft54482
- **GitHub**: https://github.com/ft54482/owl-factory
- **问题反馈**: https://github.com/ft54482/owl-factory/issues

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---

**注意**: 这是一个从中文文件夹结构迁移到英文标准结构的项目。原始的中文文件夹（`猫头鹰工场/后端程序` 和 `猫头鹰工场/前端页面`）已经重新组织为标准的英文结构（`backend/` 和 `frontend/`），以确保更好的跨平台兼容性和国际化支持。