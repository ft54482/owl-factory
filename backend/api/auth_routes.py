# -*- coding: utf-8 -*-
"""
🦉 猫头鹰工厂 - 用户认证路由
处理用户认证状态查询、用户资料管理等功能
注意：用户注册和登录现在完全由前端通过Supabase Auth处理
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from loguru import logger
from datetime import datetime

from middleware.supabase_auth import (
    get_current_user,
    get_admin_user,
    get_super_admin_user,
    get_user_profile,
    update_user_profile
)
from models.database_models import UserResponse
from config.supabase_config import supabase_manager

router = APIRouter()
security = HTTPBearer()

# 请求模型
class UpdateProfileRequest(BaseModel):
    """更新用户资料请求"""
    full_name: Optional[str] = Field(None, max_length=100, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    avatar_url: Optional[str] = Field(None, description="头像URL")

class PasswordUpdateRequest(BaseModel):
    """密码更新请求（通过Supabase Auth）"""
    new_password: str = Field(..., min_length=6, max_length=128, description="新密码")

# 响应模型
class AuthResponse(BaseModel):
    """认证响应"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    user: Optional[Dict[str, Any]] = None

@router.get("/me", response_model=AuthResponse, summary="获取当前用户信息")
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    获取当前用户信息
    
    需要在请求头中提供有效的Supabase JWT令牌
    """
    try:
        # 获取用户资料
        profile = await get_user_profile(current_user["id"])
        
        user_info = {
            "id": current_user["id"],
            "email": current_user["email"],
            "role": current_user.get("role", "user"),
            "created_at": current_user.get("created_at"),
            "last_sign_in_at": current_user.get("last_sign_in_at"),
            "profile": profile
        }
        
        return AuthResponse(
            success=True,
            message="获取用户信息成功",
            user=user_info
        )
        
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        )

@router.put("/profile", response_model=AuthResponse, summary="更新用户资料")
async def update_profile(
    profile_data: UpdateProfileRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    更新用户资料
    """
    try:
        # 更新用户资料
        updated_profile = await update_user_profile(
            current_user["id"],
            profile_data.dict(exclude_unset=True)
        )
        
        return AuthResponse(
            success=True,
            message="用户资料更新成功",
            data=updated_profile
        )
        
    except Exception as e:
        logger.error(f"更新用户资料失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户资料失败"
        )

@router.get("/status", response_model=AuthResponse, summary="检查认证状态")
async def check_auth_status(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    检查用户认证状态
    """
    return AuthResponse(
        success=True,
        message="用户已认证",
        data={
            "authenticated": True,
            "user_id": current_user["id"],
            "role": current_user.get("role", "user")
        }
    )

@router.get("/admin/status", response_model=AuthResponse, summary="检查管理员状态")
async def check_admin_status(admin_user: Dict[str, Any] = Depends(get_admin_user)):
    """
    检查管理员认证状态
    """
    return AuthResponse(
        success=True,
        message="管理员已认证",
        data={
            "authenticated": True,
            "user_id": admin_user["id"],
            "role": admin_user.get("role", "admin")
        }
    )

@router.get("/super-admin/status", response_model=AuthResponse, summary="检查超级管理员状态")
async def check_super_admin_status(super_admin: Dict[str, Any] = Depends(get_super_admin_user)):
    """
    检查超级管理员认证状态
    """
    return AuthResponse(
        success=True,
        message="超级管理员已认证",
        data={
            "authenticated": True,
            "user_id": super_admin["id"],
            "role": super_admin.get("role", "super_admin")
        }
    )