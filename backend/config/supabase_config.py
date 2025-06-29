# -*- coding: utf-8 -*-
"""
🦉 猫头鹰工厂 - Supabase配置管理
统一管理Supabase连接、认证和服务配置
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from supabase import create_client, Client
from loguru import logger

class SupabaseSettings(BaseSettings):
    """Supabase配置设置"""
    
    # Supabase基础配置
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_ANON_KEY", "")
    supabase_service_key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # 数据库配置
    database_url: str = os.getenv("DATABASE_URL", "")
    
    # JWT配置
    jwt_secret: str = os.getenv("JWT_SECRET", "your-super-secret-jwt-key")
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # 应用配置
    app_name: str = "猫头鹰工厂后台管理系统"
    app_version: str = "1.0.0"
    
    # 环境配置
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class SupabaseManager:
    """Supabase连接管理器"""
    
    def __init__(self):
        self.settings = SupabaseSettings()
        self._client: Optional[Client] = None
        self._service_client: Optional[Client] = None
        
    @property
    def client(self) -> Client:
        """获取普通客户端（使用anon key）"""
        if self._client is None:
            if not self.settings.supabase_url or not self.settings.supabase_key:
                raise ValueError("Supabase URL和ANON KEY必须配置")
            
            self._client = create_client(
                self.settings.supabase_url,
                self.settings.supabase_key
            )
            logger.info("Supabase客户端初始化成功")
            
        return self._client
    
    @property
    def service_client(self) -> Client:
        """获取服务端客户端（使用service role key）"""
        if self._service_client is None:
            if not self.settings.supabase_url or not self.settings.supabase_service_key:
                raise ValueError("Supabase URL和SERVICE ROLE KEY必须配置")
            
            self._service_client = create_client(
                self.settings.supabase_url,
                self.settings.supabase_service_key
            )
            logger.info("Supabase服务端客户端初始化成功")
            
        return self._service_client
    
    async def test_connection(self) -> bool:
        """测试Supabase连接"""
        try:
            # 测试基本连接
            response = self.client.table("user_profiles").select("*").limit(1).execute()
            logger.info("Supabase连接测试成功")
            return True
        except Exception as e:
            logger.error(f"Supabase连接测试失败: {str(e)}")
            return False
    
    def get_settings(self) -> SupabaseSettings:
        """获取配置设置"""
        return self.settings

# 全局Supabase管理器实例
supabase_manager = SupabaseManager()

# 便捷访问
def get_supabase_client() -> Client:
    """获取Supabase客户端"""
    return supabase_manager.client

def get_supabase_service_client() -> Client:
    """获取Supabase服务端客户端"""
    return supabase_manager.service_client

def get_settings() -> SupabaseSettings:
    """获取配置设置"""
    return supabase_manager.get_settings()