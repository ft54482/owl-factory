# Supabase配置文件 - 猫头鹰工厂数据库连接配置

import os
from supabase import create_client, Client
from typing import Optional
import logging

# 配置日志
logger = logging.getLogger(__name__)

class SupabaseConfig:
    """Supabase配置管理类"""
    
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.anon_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        
        if not self.url or not self.anon_key:
            raise ValueError("缺少必要的Supabase配置环境变量")
    
    def get_client(self, use_service_role: bool = False) -> Client:
        """获取Supabase客户端"""
        key = self.service_role_key if use_service_role and self.service_role_key else self.anon_key
        return create_client(self.url, key)

# 全局配置实例
_supabase_config: Optional[SupabaseConfig] = None

def get_supabase_config() -> SupabaseConfig:
    """获取Supabase配置实例"""
    global _supabase_config
    if _supabase_config is None:
        _supabase_config = SupabaseConfig()
    return _supabase_config

def get_supabase_client(use_service_role: bool = False) -> Client:
    """获取Supabase客户端实例"""
    config = get_supabase_config()
    return config.get_client(use_service_role)

# 数据库表名常量
class Tables:
    """数据库表名常量"""
    USERS = 'users'
    USER_PROFILES = 'user_profiles'
    ANALYSIS_TASKS = 'analysis_tasks'
    ANALYSIS_RESULTS = 'analysis_results'
    GPU_SERVERS = 'gpu_servers'
    GPU_USAGE_LOGS = 'gpu_usage_logs'
    RECHARGE_RECORDS = 'recharge_records'
    SYSTEM_LOGS = 'system_logs'
    ADMIN_OPERATIONS = 'admin_operations'

# 数据库初始化函数
async def init_database():
    """初始化数据库表结构"""
    try:
        client = get_supabase_client(use_service_role=True)
        
        # 检查表是否存在，如果不存在则创建
        tables_to_check = [
            Tables.USER_PROFILES,
            Tables.ANALYSIS_TASKS,
            Tables.ANALYSIS_RESULTS,
            Tables.GPU_SERVERS,
            Tables.GPU_USAGE_LOGS,
            Tables.RECHARGE_RECORDS,
            Tables.SYSTEM_LOGS,
            Tables.ADMIN_OPERATIONS
        ]
        
        for table in tables_to_check:
            try:
                # 尝试查询表，如果表不存在会抛出异常
                result = client.table(table).select('*').limit(1).execute()
                logger.info(f"表 {table} 已存在")
            except Exception as e:
                logger.warning(f"表 {table} 不存在或查询失败: {e}")
                # 这里可以添加创建表的逻辑
        
        logger.info("数据库初始化检查完成")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise

# 健康检查函数
async def check_database_health() -> bool:
    """检查数据库连接健康状态"""
    try:
        client = get_supabase_client()
        # 执行简单查询测试连接
        result = client.table(Tables.USER_PROFILES).select('id').limit(1).execute()
        return True
    except Exception as e:
        logger.error(f"数据库健康检查失败: {e}")
        return False
