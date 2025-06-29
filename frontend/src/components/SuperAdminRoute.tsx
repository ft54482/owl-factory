import React from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Loader2, Shield } from 'lucide-react'

interface SuperAdminRouteProps {
  children: React.ReactNode
}

export default function SuperAdminRoute({ children }: SuperAdminRouteProps) {
  const { user, loading, isSuperAdmin } = useAuth()

  // 显示加载状态
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">正在验证权限...</p>
        </div>
      </div>
    )
  }

  // 如果用户未登录，重定向到登录页面
  if (!user) {
    return <Navigate to="/login" replace />
  }

  // 如果不是超级管理员，显示权限不足页面
  if (!isSuperAdmin) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-md mx-auto">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Shield className="w-8 h-8 text-red-600" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">权限不足</h2>
          <p className="text-gray-600 mb-6">
            您需要超级管理员权限才能访问此页面。
          </p>
          <button
            onClick={() => window.history.back()}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            返回上一页
          </button>
        </div>
      </div>
    )
  }

  // 用户是超级管理员，渲染子组件
  return <>{children}</>
}