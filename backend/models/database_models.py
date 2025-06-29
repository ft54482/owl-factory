# -*- coding: utf-8 -*-
"""
🦉 猫头鹰工厂 - 数据库模型定义
定义所有数据库表对应的Pydantic模型
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# 枚举类型
class UserRole(str, Enum):
    """用户角色枚举"""
    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class AnalysisStatus(str, Enum):
    """分析状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class GPUStatus(str, Enum):
    """GPU状态枚举"""
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    ERROR = "error"

# 用户相关模型
class UserProfile(BaseModel):
    """用户资料模型"""
    id: str
    user_id: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    balance: float = 0.0
    total_usage: float = 0.0
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseModel):
    """用户响应模型"""
    id: str
    email: EmailStr
    role: UserRole = UserRole.USER
    created_at: datetime
    last_sign_in_at: Optional[datetime] = None
    profile: Optional[UserProfile] = None

# 分析相关模型
class AnalysisReport(BaseModel):
    """分析报告模型"""
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    video_url: str
    analysis_result: Optional[Dict[str, Any]] = None
    status: AnalysisStatus = AnalysisStatus.PENDING
    cost: float = 0.0
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

# GPU相关模型
class GPUServer(BaseModel):
    """GPU服务器模型"""
    id: str
    name: str
    host: str
    port: int = 22
    username: str
    status: GPUStatus = GPUStatus.OFFLINE
    gpu_count: int = 0
    gpu_memory_total: float = 0.0
    gpu_memory_used: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    disk_usage: float = 0.0
    last_check: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

# 充值相关模型
class RechargeRecord(BaseModel):
    """充值记录模型"""
    id: str
    user_id: str
    amount: float
    payment_method: str
    transaction_id: Optional[str] = None
    status: str = "pending"
    created_at: datetime
    updated_at: datetime

# 系统日志模型
class SystemLog(BaseModel):
    """系统日志模型"""
    id: str
    user_id: Optional[str] = None
    action: str
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

# 请求/响应模型
class CreateAnalysisRequest(BaseModel):
    """创建分析请求"""
    title: str = Field(..., max_length=200, description="分析标题")
    description: Optional[str] = Field(None, max_length=1000, description="分析描述")
    video_url: str = Field(..., description="视频URL")
    analysis_type: str = Field("standard", description="分析类型")

class UpdateAnalysisRequest(BaseModel):
    """更新分析请求"""
    title: Optional[str] = Field(None, max_length=200, description="分析标题")
    description: Optional[str] = Field(None, max_length=1000, description="分析描述")
    status: Optional[AnalysisStatus] = Field(None, description="分析状态")

class RechargeRequest(BaseModel):
    """充值请求"""
    amount: float = Field(..., gt=0, description="充值金额")
    payment_method: str = Field(..., description="支付方式")

class APIResponse(BaseModel):
    """通用API响应"""
    success: bool
    message: str
    data: Optional[Any] = None
    total: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None