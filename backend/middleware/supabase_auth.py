# -*- coding: utf-8 -*-
"""
🦉 猫头鹰工厂 - Supabase认证中间件
处理JWT令牌验证和用户权限检查
"""

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Dict, Any, Optional
from loguru import logger
from datetime import datetime

from config.supabase_config import get_supabase_client, get_supabase_service_client, get_settings

security = HTTPBearer()
settings = get_settings()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    验证Supabase JWT令牌
    """
    try:
        token = credentials.credentials
        
        # 使用Supabase客户端验证令牌
        supabase = get_supabase_client()
        
        # 设置令牌并获取用户信息
        supabase.auth.set_session(token, "")
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证令牌"
            )
        
        user = user_response.user
        
        # 返回用户信息
        return {
            "id": user.id,
            "email": user.email,
            "role": user.user_metadata.get("role", "user"),
            "created_at": user.created_at,
            "last_sign_in_at": user.last_sign_in_at,
            "user_metadata": user.user_metadata,
            "app_metadata": user.app_metadata
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"令牌验证失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证失败"
        )

async def get_current_user(user: Dict[str, Any] = Depends(verify_token)) -> Dict[str, Any]:
    """
    获取当前用户（任何已认证用户）
    """
    return user

async def get_admin_user(user: Dict[str, Any] = Depends(verify_token)) -> Dict[str, Any]:
    """
    获取管理员用户（admin或super_admin）
    """
    user_role = user.get("role", "user")
    if user_role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return user

async def get_super_admin_user(user: Dict[str, Any] = Depends(verify_token)) -> Dict[str, Any]:
    """
    获取超级管理员用户
    """
    user_role = user.get("role", "user")
    if user_role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要超级管理员权限"
        )
    return user

async def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """
    获取用户资料
    """
    try:
        supabase = get_supabase_service_client()
        
        response = supabase.table("user_profiles").select("*").eq("user_id", user_id).execute()
        
        if response.data:
            return response.data[0]
        return None
        
    except Exception as e:
        logger.error(f"获取用户资料失败: {str(e)}")
        return None

async def update_user_profile(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    更新用户资料
    """
    try:
        supabase = get_supabase_service_client()
        
        # 添加更新时间
        profile_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = supabase.table("user_profiles").update(profile_data).eq("user_id", user_id).execute()
        
        if response.data:
            return response.data[0]
        else:
            # 如果用户资料不存在，创建新的
            profile_data["user_id"] = user_id
            profile_data["created_at"] = datetime.utcnow().isoformat()
            
            create_response = supabase.table("user_profiles").insert(profile_data).execute()
            return create_response.data[0]
            
    except Exception as e:
        logger.error(f"更新用户资料失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新用户资料失败"
        )