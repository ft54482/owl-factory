# 部署指南 (Deployment Guide)

本文档详细说明了猫头鹰工厂项目的部署流程和配置要求。

## 📋 部署前准备

### 系统要求

#### 最低配置
- **CPU**: 4核心
- **内存**: 8GB RAM
- **存储**: 100GB SSD
- **操作系统**: Ubuntu 20.04+ / CentOS 8+ / Windows Server 2019+

#### 推荐配置
- **CPU**: 8核心以上
- **内存**: 16GB RAM以上
- **存储**: 500GB SSD以上
- **GPU**: NVIDIA GPU (用于AI加速)
- **网络**: 100Mbps以上带宽

### 软件依赖

```bash
# Docker 和 Docker Compose
Docker 20.10+
Docker Compose 2.0+

# 开发环境 (可选)
Node.js 18+
Python 3.11+
Nginx 1.20+
```

## 🚀 快速部署

### 1. 环境准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 添加用户到 docker 组
sudo usermod -aG docker $USER
newgrp docker
```

### 2. 项目部署

```bash
# 克隆项目
git clone https://github.com/ft54482/owl-factory.git
cd owl-factory

# 配置环境变量
cp .env.example .env
nano .env  # 编辑配置文件

# 启动服务
docker-compose up -d

# 检查服务状态
docker-compose ps
```

### 3. 验证部署

```bash
# 检查服务健康状态
curl http://localhost:8000/health
curl http://localhost:3000

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

## ⚙️ 详细配置

### 环境变量配置

#### 必需配置

```bash
# Supabase 配置
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# JWT 配置
JWT_SECRET_KEY=your_super_secret_jwt_key_here

# 基础配置
ENVIRONMENT=production
DEBUG=false
```

#### GPU 集群配置

```bash
# GPU 服务器配置
GPU_SERVERS='[
  {
    "id": "gpu-worker-01",
    "host": "192.168.1.100",
    "port": 22,
    "username": "gpu_user",
    "gpu_count": 4,
    "status": "active"
  },
  {
    "id": "gpu-worker-02",
    "host": "192.168.1.101",
    "port": 22,
    "username": "gpu_user",
    "gpu_count": 8,
    "status": "active"
  }
]'
```

#### 外部API配置

```bash
# 视频平台 API
DOUYIN_API_KEY=your_douyin_api_key
XIAOHONGSHU_API_KEY=your_xiaohongshu_api_key
BILIBILI_API_KEY=your_bilibili_api_key
TIKTOK_API_KEY=your_tiktok_api_key
```

### Nginx 配置

创建 `nginx/nginx.conf` 文件：

```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }
    
    upstream frontend {
        server frontend:3000;
    }
    
    # 前端服务
    server {
        listen 80;
        server_name app.yourdomain.com;
        
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    
    # 后端API服务
    server {
        listen 80;
        server_name api.yourdomain.com;
        
        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # 文件上传大小限制
        client_max_body_size 500M;
    }
}
```

## 🔒 生产环境配置

### SSL/TLS 配置

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取 SSL 证书
sudo certbot --nginx -d api.yourdomain.com -d app.yourdomain.com

# 自动续期
sudo crontab -e
# 添加以下行
0 12 * * * /usr/bin/certbot renew --quiet
```

### 防火墙配置

```bash
# 配置 UFW 防火墙
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 3001/tcp  # Grafana
sudo ufw allow 9090/tcp  # Prometheus
```

### 数据备份

```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/owl-factory-$DATE"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose exec -T postgres pg_dump -U postgres owl_factory > $BACKUP_DIR/database.sql

# 备份 Redis 数据
docker-compose exec -T redis redis-cli BGSAVE
docker cp $(docker-compose ps -q redis):/data/dump.rdb $BACKUP_DIR/

# 备份上传文件
cp -r uploads $BACKUP_DIR/
cp -r reports $BACKUP_DIR/

# 压缩备份
tar -czf /backup/owl-factory-$DATE.tar.gz -C /backup owl-factory-$DATE
rm -rf $BACKUP_DIR

echo "备份完成: /backup/owl-factory-$DATE.tar.gz"
EOF

chmod +x backup.sh

# 设置定时备份
crontab -e
# 添加以下行 (每天凌晨2点备份)
0 2 * * * /path/to/backup.sh
```

## 📊 监控配置

### Prometheus 配置

创建 `config/prometheus.yml`：

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
  
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
  
  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
  
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']
```

### Grafana 配置

创建 `config/grafana/datasources/prometheus.yml`：

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

## 🔧 性能优化

### Docker 优化

```bash
# 配置 Docker daemon
sudo nano /etc/docker/daemon.json
```

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
```

### 系统优化

```bash
# 优化系统参数
sudo nano /etc/sysctl.conf
```

```bash
# 网络优化
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216

# 文件描述符限制
fs.file-max = 2097152

# 应用更改
sudo sysctl -p
```

## 🚨 故障排除

### 常见问题

#### 1. 服务启动失败

```bash
# 检查服务状态
docker-compose ps

# 查看详细日志
docker-compose logs service_name

# 重启服务
docker-compose restart service_name

# 完全重建
docker-compose down
docker-compose up -d --build
```

#### 2. 数据库连接问题

```bash
# 检查 Supabase 连接
curl -H "apikey: your_anon_key" "https://your-project.supabase.co/rest/v1/"

# 检查本地数据库
docker-compose exec postgres psql -U postgres -d owl_factory -c "\dt"
```

#### 3. GPU 不可用

```bash
# 检查 NVIDIA 驱动
nvidia-smi

# 检查 Docker GPU 支持
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi

# 安装 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

#### 4. 内存不足

```bash
# 检查内存使用
free -h
docker stats

# 清理 Docker 资源
docker system prune -a
docker volume prune

# 增加 swap 空间
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 日志分析

```bash
# 实时查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 查看最近的错误日志
docker-compose logs --tail=100 backend | grep ERROR

# 导出日志到文件
docker-compose logs > deployment.log
```

## 📈 扩展部署

### 水平扩展

```bash
# 扩展后端服务
docker-compose up -d --scale backend=3

# 扩展任务工作进程
docker-compose up -d --scale task-worker=5

# 使用 Docker Swarm 集群
docker swarm init
docker stack deploy -c docker-compose.yml owl-factory
```

### 负载均衡

```nginx
# Nginx 负载均衡配置
upstream backend_cluster {
    least_conn;
    server backend_1:8000 weight=1;
    server backend_2:8000 weight=1;
    server backend_3:8000 weight=1;
}

server {
    location /api {
        proxy_pass http://backend_cluster;
    }
}
```

## 🔄 更新部署

### 滚动更新

```bash
# 拉取最新代码
git pull origin main

# 重建并更新服务
docker-compose build
docker-compose up -d

# 零停机更新
docker-compose up -d --no-deps --build backend
docker-compose up -d --no-deps --build frontend
```

### 版本回滚

```bash
# 查看提交历史
git log --oneline

# 回滚到指定版本
git checkout <commit_hash>
docker-compose down
docker-compose up -d --build
```

---

**注意**: 在生产环境部署前，请确保已经完成所有安全配置和性能优化设置。建议先在测试环境中验证部署流程。