# 智能分析API - 猫头鹰工厂核心分析服务
# 提供单视频分析和完整账号分析功能

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
import asyncio
import uuid
from datetime import datetime
import json

# 导入依赖服务
from ..middleware.supabase_auth import get_current_user
from ..services.gpu_monitor_service import GPUMonitorService
from ..config.supabase_config import get_supabase_client

router = APIRouter(prefix="/api/analysis", tags=["智能分析"])

# 数据模型定义
class VideoAnalysisRequest(BaseModel):
    """单视频分析请求模型"""
    video_url: HttpUrl
    platform: str  # 平台类型：douyin, xiaohongshu, bilibili, tiktok
    analysis_type: str = "standard"  # 分析类型：standard, deep, quick
    options: Optional[Dict[str, Any]] = None

class AccountAnalysisRequest(BaseModel):
    """完整账号分析请求模型"""
    account_url: HttpUrl
    platform: str
    analysis_depth: str = "complete"  # 分析深度：complete, recent, sample
    video_limit: Optional[int] = None  # 视频数量限制
    options: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    """分析响应模型"""
    task_id: str
    status: str  # pending, processing, completed, failed
    message: str
    estimated_time: Optional[int] = None  # 预估完成时间（秒）

class AnalysisResult(BaseModel):
    """分析结果模型"""
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    processing_time: Optional[float] = None

# 全局任务存储（生产环境应使用Redis或数据库）
analysis_tasks = {}

# 平台检测器
def detect_platform(url: str) -> str:
    """检测URL所属平台"""
    url_lower = url.lower()
    if 'douyin.com' in url_lower or 'dy.com' in url_lower:
        return 'douyin'
    elif 'xiaohongshu.com' in url_lower or 'xhs.com' in url_lower:
        return 'xiaohongshu'
    elif 'bilibili.com' in url_lower or 'b23.tv' in url_lower:
        return 'bilibili'
    elif 'tiktok.com' in url_lower:
        return 'tiktok'
    else:
        return 'unknown'

# URL类型检测器
def detect_url_type(url: str) -> str:
    """检测URL类型：video或profile"""
    url_lower = url.lower()
    # 视频URL特征
    video_patterns = ['/video/', '/v/', '/play/', '/watch?v=', '/p/']
    # 用户主页URL特征
    profile_patterns = ['/user/', '/u/', '/profile/', '/channel/', '/@']
    
    for pattern in video_patterns:
        if pattern in url_lower:
            return 'video'
    
    for pattern in profile_patterns:
        if pattern in url_lower:
            return 'profile'
    
    return 'unknown'

@router.post("/single-video", response_model=AnalysisResponse)
async def analyze_single_video(
    request: VideoAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """单视频分析接口"""
    try:
        # 生成任务ID
        task_id = str(uuid.uuid4())
        
        # 验证平台
        detected_platform = detect_platform(str(request.video_url))
        if detected_platform == 'unknown':
            raise HTTPException(status_code=400, detail="不支持的视频平台")
        
        # 验证URL类型
        url_type = detect_url_type(str(request.video_url))
        if url_type != 'video':
            raise HTTPException(status_code=400, detail="请提供有效的视频URL")
        
        # 检查GPU资源
        gpu_service = GPUMonitorService()
        available_gpu = await gpu_service.get_available_gpu()
        if not available_gpu:
            raise HTTPException(status_code=503, detail="GPU资源暂时不可用，请稍后重试")
        
        # 创建任务记录
        task_data = {
            'task_id': task_id,
            'user_id': current_user['id'],
            'type': 'single_video',
            'status': 'pending',
            'video_url': str(request.video_url),
            'platform': detected_platform,
            'analysis_type': request.analysis_type,
            'options': request.options or {},
            'created_at': datetime.utcnow(),
            'gpu_id': available_gpu['id']
        }
        
        analysis_tasks[task_id] = task_data
        
        # 启动后台分析任务
        background_tasks.add_task(
            process_single_video_analysis,
            task_id,
            task_data
        )
        
        # 预估处理时间（基于分析类型）
        time_estimates = {
            'quick': 30,
            'standard': 120,
            'deep': 300
        }
        estimated_time = time_estimates.get(request.analysis_type, 120)
        
        return AnalysisResponse(
            task_id=task_id,
            status="pending",
            message="视频分析任务已创建，正在处理中...",
            estimated_time=estimated_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建分析任务失败: {str(e)}")

@router.post("/complete-account", response_model=AnalysisResponse)
async def analyze_complete_account(
    request: AccountAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """完整账号分析接口"""
    try:
        # 生成任务ID
        task_id = str(uuid.uuid4())
        
        # 验证平台
        detected_platform = detect_platform(str(request.account_url))
        if detected_platform == 'unknown':
            raise HTTPException(status_code=400, detail="不支持的账号平台")
        
        # 验证URL类型
        url_type = detect_url_type(str(request.account_url))
        if url_type != 'profile':
            raise HTTPException(status_code=400, detail="请提供有效的账号主页URL")
        
        # 检查GPU资源（账号分析需要更多资源）
        gpu_service = GPUMonitorService()
        available_gpus = await gpu_service.get_available_gpus(min_count=2)
        if len(available_gpus) < 2:
            raise HTTPException(status_code=503, detail="账号分析需要更多GPU资源，请稍后重试")
        
        # 创建任务记录
        task_data = {
            'task_id': task_id,
            'user_id': current_user['id'],
            'type': 'complete_account',
            'status': 'pending',
            'account_url': str(request.account_url),
            'platform': detected_platform,
            'analysis_depth': request.analysis_depth,
            'video_limit': request.video_limit,
            'options': request.options or {},
            'created_at': datetime.utcnow(),
            'gpu_ids': [gpu['id'] for gpu in available_gpus]
        }
        
        analysis_tasks[task_id] = task_data
        
        # 启动后台分析任务
        background_tasks.add_task(
            process_account_analysis,
            task_id,
            task_data
        )
        
        # 预估处理时间（基于分析深度和视频数量）
        base_time = {
            'recent': 300,
            'sample': 600,
            'complete': 1800
        }
        estimated_time = base_time.get(request.analysis_depth, 600)
        if request.video_limit:
            estimated_time = min(estimated_time, request.video_limit * 30)
        
        return AnalysisResponse(
            task_id=task_id,
            status="pending",
            message="账号分析任务已创建，正在处理中...",
            estimated_time=estimated_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建分析任务失败: {str(e)}")

@router.get("/status/{task_id}", response_model=AnalysisResult)
async def get_analysis_status(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取分析任务状态"""
    if task_id not in analysis_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task_data = analysis_tasks[task_id]
    
    # 验证用户权限
    if task_data['user_id'] != current_user['id'] and current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="无权访问此任务")
    
    return AnalysisResult(
        task_id=task_id,
        status=task_data['status'],
        result=task_data.get('result'),
        error=task_data.get('error'),
        created_at=task_data['created_at'],
        completed_at=task_data.get('completed_at'),
        processing_time=task_data.get('processing_time')
    )

@router.get("/result/{task_id}")
async def get_analysis_result(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取分析结果详情"""
    if task_id not in analysis_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task_data = analysis_tasks[task_id]
    
    # 验证用户权限
    if task_data['user_id'] != current_user['id'] and current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="无权访问此任务")
    
    if task_data['status'] != 'completed':
        raise HTTPException(status_code=400, detail="任务尚未完成")
    
    return task_data.get('result', {})

@router.get("/history")
async def get_analysis_history(
    page: int = 1,
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """获取用户分析历史"""
    user_tasks = [
        task for task in analysis_tasks.values()
        if task['user_id'] == current_user['id']
    ]
    
    # 按创建时间倒序排列
    user_tasks.sort(key=lambda x: x['created_at'], reverse=True)
    
    # 分页
    start = (page - 1) * limit
    end = start + limit
    paginated_tasks = user_tasks[start:end]
    
    return {
        'tasks': paginated_tasks,
        'total': len(user_tasks),
        'page': page,
        'limit': limit,
        'has_more': end < len(user_tasks)
    }

# 后台处理函数
async def process_single_video_analysis(task_id: str, task_data: dict):
    """处理单视频分析任务"""
    try:
        # 更新任务状态
        analysis_tasks[task_id]['status'] = 'processing'
        analysis_tasks[task_id]['started_at'] = datetime.utcnow()
        
        # 模拟分析过程（实际实现中会调用AI服务）
        await asyncio.sleep(5)  # 模拟处理时间
        
        # 模拟分析结果
        result = {
            'video_info': {
                'title': '示例视频标题',
                'duration': 120,
                'platform': task_data['platform'],
                'url': task_data['video_url']
            },
            'transcript': {
                'text': '这是视频的转录文本...',
                'segments': [
                    {'start': 0, 'end': 10, 'text': '开头部分'},
                    {'start': 10, 'end': 20, 'text': '中间部分'}
                ]
            },
            'analysis': {
                'sentiment': 'positive',
                'topics': ['科技', '教育'],
                'keywords': ['AI', '机器学习', '深度学习'],
                'summary': '这是一个关于AI技术的教育视频...'
            },
            'metrics': {
                'engagement_score': 8.5,
                'content_quality': 9.0,
                'educational_value': 8.8
            }
        }
        
        # 更新任务完成状态
        completed_at = datetime.utcnow()
        analysis_tasks[task_id].update({
            'status': 'completed',
            'result': result,
            'completed_at': completed_at,
            'processing_time': (completed_at - analysis_tasks[task_id]['started_at']).total_seconds()
        })
        
    except Exception as e:
        # 处理错误
        analysis_tasks[task_id].update({
            'status': 'failed',
            'error': str(e),
            'completed_at': datetime.utcnow()
        })

async def process_account_analysis(task_id: str, task_data: dict):
    """处理完整账号分析任务"""
    try:
        # 更新任务状态
        analysis_tasks[task_id]['status'] = 'processing'
        analysis_tasks[task_id]['started_at'] = datetime.utcnow()
        
        # 模拟账号分析过程
        await asyncio.sleep(10)  # 模拟处理时间
        
        # 模拟分析结果
        result = {
            'account_info': {
                'username': '示例用户',
                'platform': task_data['platform'],
                'url': task_data['account_url'],
                'follower_count': 10000,
                'video_count': 50
            },
            'content_analysis': {
                'main_topics': ['科技', '教育', '生活'],
                'content_style': 'educational',
                'posting_frequency': 'daily',
                'engagement_rate': 0.085
            },
            'video_summaries': [
                {
                    'title': '视频1',
                    'duration': 120,
                    'views': 5000,
                    'sentiment': 'positive'
                }
            ],
            'insights': {
                'growth_trend': 'increasing',
                'best_performing_content': '教育类视频',
                'audience_engagement': 'high',
                'content_recommendations': [
                    '增加互动性内容',
                    '保持发布频率',
                    '关注热门话题'
                ]
            },
            'metrics': {
                'overall_score': 8.7,
                'content_quality': 9.1,
                'audience_engagement': 8.5,
                'growth_potential': 8.9
            }
        }
        
        # 更新任务完成状态
        completed_at = datetime.utcnow()
        analysis_tasks[task_id].update({
            'status': 'completed',
            'result': result,
            'completed_at': completed_at,
            'processing_time': (completed_at - analysis_tasks[task_id]['started_at']).total_seconds()
        })
        
    except Exception as e:
        # 处理错误
        analysis_tasks[task_id].update({
            'status': 'failed',
            'error': str(e),
            'completed_at': datetime.utcnow()
        })

# 管理员接口
@router.get("/admin/tasks")
async def get_all_tasks(
    page: int = 1,
    limit: int = 50,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """管理员获取所有分析任务"""
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    tasks = list(analysis_tasks.values())
    
    # 状态过滤
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    
    # 按创建时间倒序排列
    tasks.sort(key=lambda x: x['created_at'], reverse=True)
    
    # 分页
    start = (page - 1) * limit
    end = start + limit
    paginated_tasks = tasks[start:end]
    
    return {
        'tasks': paginated_tasks,
        'total': len(tasks),
        'page': page,
        'limit': limit,
        'has_more': end < len(tasks)
    }

@router.delete("/admin/tasks/{task_id}")
async def delete_task(
    task_id: str,
    current_user: dict = Depends(get_current_user)
):
    """管理员删除分析任务"""
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    if task_id not in analysis_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    del analysis_tasks[task_id]
    return {'message': '任务已删除'}
