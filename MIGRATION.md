# 项目迁移指南 (Migration Guide)

本文档详细说明了如何从原始的中文文件夹结构迁移到标准化的英文项目结构。

## 📋 迁移概述

### 迁移原因

1. **GitHub兼容性**: GitHub不完全支持中文文件夹名称，可能导致：
   - 文件路径显示异常
   - 克隆和同步问题
   - CI/CD流程中断
   - 跨平台兼容性问题

2. **国际化标准**: 使用英文文件夹名称符合国际化开发标准

3. **团队协作**: 便于国际团队成员理解和协作

4. **工具兼容性**: 确保各种开发工具和部署平台的兼容性

### 迁移映射

| 原始结构 (中文) | 新结构 (英文) | 说明 |
|----------------|---------------|------|
| `猫头鹰工场/` | `owl-factory/` | 项目根目录 |
| `后端程序/` | `backend/` | 后端服务代码 |
| `前端页面/` | `frontend/` | 前端应用代码 |
| `智能分析API.py` | `intelligent_analysis_api.py` | 智能分析API文件 |

## 🚀 自动迁移脚本

### Windows 迁移脚本

创建 `migrate.bat` 文件：

```batch
@echo off
echo 开始迁移猫头鹰工厂项目结构...

:: 创建新的英文目录结构
mkdir owl-factory
cd owl-factory

:: 迁移后端代码
echo 迁移后端代码...
mkdir backend
xcopy "..\猫头鹰工场\后端程序\*" "backend\" /E /I /Y

:: 迁移前端代码
echo 迁移前端代码...
mkdir frontend
xcopy "..\猫头鹰工场\前端页面\*" "frontend\" /E /I /Y

:: 重命名特殊文件
if exist "backend\api\智能分析API.py" (
    ren "backend\api\智能分析API.py" "intelligent_analysis_api.py"
)

:: 创建项目配置文件
echo 创建项目配置文件...
copy NUL .gitignore
copy NUL README.md
copy NUL docker-compose.yml
copy NUL .env.example

echo 迁移完成！新项目位于: owl-factory/
echo 请检查文件完整性并更新相关配置。
pause
```

### Linux/Mac 迁移脚本

创建 `migrate.sh` 文件：

```bash
#!/bin/bash

echo "开始迁移猫头鹰工厂项目结构..."

# 创建新的英文目录结构
mkdir -p owl-factory
cd owl-factory

# 迁移后端代码
echo "迁移后端代码..."
mkdir -p backend
cp -r "../猫头鹰工场/后端程序/"* backend/ 2>/dev/null || true

# 迁移前端代码
echo "迁移前端代码..."
mkdir -p frontend
cp -r "../猫头鹰工场/前端页面/"* frontend/ 2>/dev/null || true

# 重命名特殊文件
if [ -f "backend/api/智能分析API.py" ]; then
    mv "backend/api/智能分析API.py" "backend/api/intelligent_analysis_api.py"
fi

# 创建项目配置文件
echo "创建项目配置文件..."
touch .gitignore
touch README.md
touch docker-compose.yml
touch .env.example

# 设置权限
chmod +x backend/*.py 2>/dev/null || true
chmod +x frontend/scripts/* 2>/dev/null || true

echo "迁移完成！新项目位于: owl-factory/"
echo "请检查文件完整性并更新相关配置。"
```

## 📝 手动迁移步骤

### 1. 创建新项目结构

```bash
# 创建新的项目目录
mkdir owl-factory
cd owl-factory

# 创建标准目录结构
mkdir -p backend/{api,config,database,middleware,models,services,scripts}
mkdir -p frontend/{src,public}
mkdir -p gpu-cluster
mkdir -p nginx
mkdir -p config
mkdir -p logs
mkdir -p reports
mkdir -p uploads
```

### 2. 迁移后端代码

```bash
# 复制后端文件
cp -r "../猫头鹰工场/后端程序/"* backend/

# 重命名中文文件
mv "backend/api/智能分析API.py" "backend/api/intelligent_analysis_api.py"

# 检查文件编码
file backend/api/*.py
```

### 3. 迁移前端代码

```bash
# 复制前端文件
cp -r "../猫头鹰工场/前端页面/"* frontend/

# 检查 package.json
cat frontend/package.json
```

### 4. 更新文件引用

#### 后端文件引用更新

```python
# 更新 main.py 中的导入路径
# 原来:
# from api.智能分析API import router as analysis_router

# 更新为:
from api.intelligent_analysis_api import router as analysis_router
```

#### 前端文件引用更新

```typescript
// 更新 API 调用路径
// 检查 src/services/ 中的 API 端点配置
```

### 5. 更新配置文件

#### 更新 Docker 配置

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🔧 配置更新

### 1. 环境变量更新

```bash
# .env 文件路径更新
# 原来的相对路径需要调整
UPLOAD_DIR=./uploads
REPORT_DIR=./reports
LOG_DIR=./logs
```

### 2. API 路径更新

```python
# backend/main.py
from fastapi import FastAPI
from api import (
    admin_routes,
    auth_routes,
    gpu_routes,
    log_routes,
    recharge_routes,
    user_routes,
    intelligent_analysis_api  # 更新导入名称
)

app = FastAPI(title="猫头鹰工厂 API")

# 注册路由
app.include_router(intelligent_analysis_api.router, prefix="/api/analysis")
```

### 3. 前端配置更新

```typescript
// frontend/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

## 🧪 迁移验证

### 1. 文件完整性检查

```bash
# 检查文件数量
echo "原始后端文件数量:"
find "../猫头鹰工场/后端程序" -type f | wc -l

echo "迁移后后端文件数量:"
find "backend" -type f | wc -l

echo "原始前端文件数量:"
find "../猫头鹰工场/前端页面" -type f | wc -l

echo "迁移后前端文件数量:"
find "frontend" -type f | wc -l
```

### 2. 代码语法检查

```bash
# Python 语法检查
python -m py_compile backend/main.py
python -m py_compile backend/api/intelligent_analysis_api.py

# TypeScript 语法检查
cd frontend
npm run type-check
```

### 3. 功能测试

```bash
# 启动后端服务
cd backend
python main.py

# 启动前端服务
cd frontend
npm run dev

# 测试 API 端点
curl http://localhost:8000/health
curl http://localhost:8000/api/analysis/status
```

## 🔄 Git 迁移

### 1. 初始化新仓库

```bash
# 在新项目目录中初始化 Git
cd owl-factory
git init

# 添加 .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Runtime
uploads/
reports/
cache/

# Docker
.dockerignore
EOF
```

### 2. 提交初始版本

```bash
# 添加所有文件
git add .

# 提交初始版本
git commit -m "Initial commit: 迁移项目到标准英文结构

- 将中文文件夹重命名为英文
- 更新文件引用和导入路径
- 添加 Docker 配置
- 添加环境变量模板
- 更新项目文档"

# 添加远程仓库
git remote add origin https://github.com/ft54482/owl-factory.git

# 推送到远程仓库
git push -u origin main
```

### 3. 保留历史记录 (可选)

如果需要保留原始项目的 Git 历史记录：

```bash
# 克隆原始仓库
git clone <original-repo-url> temp-repo
cd temp-repo

# 使用 git-filter-repo 重写历史
# 安装: pip install git-filter-repo
git filter-repo --path-rename 猫头鹰工场/后端程序/:backend/
git filter-repo --path-rename 猫头鹰工场/前端页面/:frontend/

# 合并到新仓库
cd ../owl-factory
git remote add old-repo ../temp-repo
git fetch old-repo
git merge old-repo/main --allow-unrelated-histories
```

## 📋 迁移检查清单

### 文件迁移
- [ ] 后端代码完整迁移
- [ ] 前端代码完整迁移
- [ ] 配置文件更新
- [ ] 中文文件名重命名
- [ ] 文件权限设置

### 代码更新
- [ ] 导入路径更新
- [ ] API 路径更新
- [ ] 配置文件路径更新
- [ ] 环境变量更新
- [ ] 数据库连接配置

### 功能验证
- [ ] 后端服务启动正常
- [ ] 前端应用启动正常
- [ ] API 端点响应正常
- [ ] 数据库连接正常
- [ ] 文件上传功能正常

### 部署配置
- [ ] Docker 配置更新
- [ ] Nginx 配置更新
- [ ] 环境变量配置
- [ ] SSL 证书配置
- [ ] 监控配置更新

### 文档更新
- [ ] README.md 更新
- [ ] API 文档更新
- [ ] 部署文档更新
- [ ] 开发文档更新
- [ ] 迁移文档创建

## 🚨 常见问题

### 1. 文件编码问题

```bash
# 检查文件编码
file -bi backend/api/*.py

# 转换编码 (如果需要)
iconv -f GBK -t UTF-8 input.py > output.py
```

### 2. 路径分隔符问题

```python
# 使用 os.path.join 或 pathlib 确保跨平台兼容
import os
from pathlib import Path

# 推荐使用 pathlib
upload_path = Path("uploads") / "videos" / filename
```

### 3. 导入路径错误

```python
# 检查 Python 路径
import sys
print(sys.path)

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
```

### 4. 前端构建失败

```bash
# 清理缓存
npm cache clean --force
rm -rf node_modules package-lock.json
npm install

# 检查 Node.js 版本
node --version
npm --version
```

## 📞 支持

如果在迁移过程中遇到问题，请：

1. 检查本文档的常见问题部分
2. 查看项目的 GitHub Issues
3. 联系项目维护者
4. 提交新的 Issue 描述问题

---

**注意**: 迁移完成后，建议保留原始项目备份一段时间，确保新结构完全正常工作后再删除。