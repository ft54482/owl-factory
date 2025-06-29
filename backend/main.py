# -*- coding: utf-8 -*-
"""
🦉 猫头鹰工厂 - 后台管理系统主应用
基于FastAPI + Supabase的完整后端解决方案
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
from loguru import logger
import sys

# 配置日志
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/app.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    rotation="1 day",
    retention="30 days"
)

# 导入配置和服务
from config.supabase_config import settings, supabase_manager
from services.recharge_service import recharge_service
from services.gpu_monitor_service import gpu_monitor_service

# 导入API路由
from api.auth_routes import router as auth_router
from api.user_routes import router as user_router
from api.recharge_routes import router as recharge_router
from api.gpu_routes import router as gpu_router
from api.admin_routes import router as admin_router
from api.log_routes import router as log_router

# 导入Supabase认证中间件
from middleware.supabase_auth import get_current_user, get_admin_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 猫头鹰工厂后台管理系统启动中...")
    
    try:
        # 测试Supabase连接
        if supabase_manager.test_connection():
            logger.info("✅ Supabase连接测试成功")
        else:
            logger.warning("⚠️ Supabase连接测试失败")
        
        # 同步GPU服务器配置
        sync_result = await gpu_monitor_service.sync_gpu_servers_to_database()
        if sync_result["success"]:
            logger.info(f"✅ GPU服务器配置同步成功: {sync_result['message']}")
        else:
            logger.warning(f"⚠️ GPU服务器配置同步失败: {sync_result['message']}")
        
        logger.info("🎉 系统启动完成")
        
    except Exception as e:
        logger.error(f"❌ 系统启动失败: {e}")
    
    yield
    
    # 关闭时执行
    logger.info("👋 猫头鹰工厂后台管理系统关闭")

# 创建FastAPI应用
app = FastAPI(
    title="猫头鹰工厂后台管理系统",
    description="基于Supabase的完整后端管理解决方案",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://your-frontend-domain.com"  # 生产环境域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加受信任主机中间件
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.your-domain.com"]
)

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"全局异常: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误"}
    )

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "service": "猫头鹰工厂后台管理系统"
    }

# 根端点
@app.get("/")
async def root():
    """根端点"""
    return {
        "message": "🦉 欢迎使用猫头鹰工厂后台管理系统",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# 注册API路由
app.include_router(auth_router, prefix="/api/auth", tags=["认证"])
app.include_router(user_router, prefix="/api/users", tags=["用户管理"])
app.include_router(recharge_router, prefix="/api/recharge", tags=["充值管理"])
app.include_router(gpu_router, prefix="/api/gpu", tags=["GPU管理"])
app.include_router(admin_router, prefix="/api/admin", tags=["管理员"])
app.include_router(log_router, prefix="/api/logs", tags=["日志管理"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )