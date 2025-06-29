import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Search, 
  Download, 
  Eye, 
  Trash2,
  Calendar,
  FileText,
  Star,
  Clock,
  TrendingUp,
  User
} from 'lucide-react'
import { useAppStore } from '@/store'
import { Link } from 'react-router-dom'

interface AnalysisReport {
  id: string
  title: string
  url: string
  author: string
  platform: string
  createdAt: string
  status: 'completed' | 'processing' | 'failed'
  score: number
  category: string
  tags: string[]
  thumbnail?: string
  duration?: number
  viewCount?: number
}

export default function ReportManagement() {
  const { tasks, results } = useAppStore()
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedStatus, setSelectedStatus] = useState('all')
  const [selectedPlatform, setSelectedPlatform] = useState('all')
  const [sortBy, setSortBy] = useState('createdAt')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')

  // 将任务转换为报告格式
  const reports: AnalysisReport[] = tasks
    .filter(task => task.status === 'completed' || task.status === 'error')
    .map(task => {
      // 查找对应的结果
      const result = results.find(r => r.taskId === task.id)
      const videoInfo = result?.videoInfo
      
      return {
        id: task.id,
        title: videoInfo?.title || task.title || '未知标题',
        url: task.url,
        author: videoInfo?.author || '未知作者',
        platform: videoInfo?.platform || '未知平台',
        createdAt: task.createdAt.toISOString(),
        status: task.status as 'completed' | 'failed',
        score: Math.floor(Math.random() * 100), // 模拟评分
        category: 'general',
        tags: ['视频分析', '内容分析'],
        thumbnail: videoInfo?.thumbnail,
        duration: videoInfo?.duration,
        viewCount: Math.floor(Math.random() * 100000),
      }
    })

  const statusOptions = [
    { value: 'all', label: '全部状态' },
    { value: 'completed', label: '已完成' },
    { value: 'failed', label: '失败' },
  ]

  const platformOptions = [
    { value: 'all', label: '全部平台' },
    { value: 'TikTok', label: '抖音' },
    { value: '小红书', label: '小红书' },
    { value: 'B站', label: 'B站' },
  ]

  const sortOptions = [
    { value: 'createdAt', label: '创建时间' },
    { value: 'score', label: '评分' },
    { value: 'title', label: '标题' },
    { value: 'author', label: '作者' },
  ]

  const filteredReports = reports
    .filter(report => {
      const matchesSearch = report.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           report.author.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesStatus = selectedStatus === 'all' || report.status === selectedStatus
      const matchesPlatform = selectedPlatform === 'all' || report.platform === selectedPlatform
      return matchesSearch && matchesStatus && matchesPlatform
    })
    .sort((a, b) => {
      let aValue = a[sortBy as keyof AnalysisReport]
      let bValue = b[sortBy as keyof AnalysisReport]
      
      // 处理undefined值
      if (aValue === undefined) aValue = ''
      if (bValue === undefined) bValue = ''
      
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return sortOrder === 'asc' 
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue)
      }
      
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortOrder === 'asc' ? aValue - bValue : bValue - aValue
      }
      
      return 0
    })

  const handleDownload = (report: AnalysisReport) => {
    // 实现下载功能
    console.log('下载报告:', report.id)
  }

  const handleDelete = (reportId: string) => {
    // 实现删除功能
    console.log('删除报告:', reportId)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-6 py-8">
        {/* 页面标题 */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-2">报告管理</h1>
          <p className="text-gray-600">管理和查看所有分析报告</p>
        </motion.div>

        {/* 统计卡片 */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
          >
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <FileText className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">总报告数</p>
                <p className="text-2xl font-bold text-gray-900">{reports.length}</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
          >
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <Star className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">已完成</p>
                <p className="text-2xl font-bold text-gray-900">
                  {reports.filter(r => r.status === 'completed').length}
                </p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
          >
            <div className="flex items-center">
              <div className="p-2 bg-red-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-red-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">平均评分</p>
                <p className="text-2xl font-bold text-gray-900">
                  {reports.length > 0 ? Math.round(reports.reduce((sum, r) => sum + r.score, 0) / reports.length) : 0}
                </p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-xl shadow-sm border border-gray-100 p-6"
          >
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Calendar className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">本月报告</p>
                <p className="text-2xl font-bold text-gray-900">
                  {reports.filter(r => new Date(r.createdAt).getMonth() === new Date().getMonth()).length}
                </p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* 搜索和筛选 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-8"
        >
          <div className="flex flex-col lg:flex-row gap-4">
            {/* 搜索框 */}
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="搜索报告标题或作者..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* 筛选器 */}
            <div className="flex gap-4">
              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {statusOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>

              <select
                value={selectedPlatform}
                onChange={(e) => setSelectedPlatform(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {platformOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>

              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {sortOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>

              <button
                onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
                className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
              >
                {sortOrder === 'asc' ? '↑' : '↓'}
              </button>
            </div>
          </div>
        </motion.div>

        {/* 报告列表 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden"
        >
          {filteredReports.length === 0 ? (
            <div className="p-12 text-center">
              <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">暂无报告</h3>
              <p className="text-gray-500">还没有生成任何分析报告</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      报告信息
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      平台
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      状态
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      评分
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      创建时间
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      操作
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {filteredReports.map((report, index) => (
                    <motion.tr
                      key={report.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className="hover:bg-gray-50"
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          {report.thumbnail && (
                            <img
                              src={report.thumbnail}
                              alt={report.title}
                              className="w-12 h-12 rounded-lg object-cover mr-4"
                            />
                          )}
                          <div>
                            <div className="text-sm font-medium text-gray-900 max-w-xs truncate">
                              {report.title}
                            </div>
                            <div className="text-sm text-gray-500 flex items-center mt-1">
                              <User className="w-4 h-4 mr-1" />
                              {report.author}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {report.platform}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          report.status === 'completed'
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {report.status === 'completed' ? '已完成' : '失败'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <Star className="w-4 h-4 text-yellow-400 mr-1" />
                          <span className="text-sm text-gray-900">{report.score}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-1" />
                          {new Date(report.createdAt).toLocaleDateString()}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex items-center space-x-2">
                          <Link
                            to={`/report/${report.id}`}
                            className="text-blue-600 hover:text-blue-900 p-1 rounded transition-colors"
                          >
                            <Eye className="w-4 h-4" />
                          </Link>
                          <button
                            onClick={() => handleDownload(report)}
                            className="text-green-600 hover:text-green-900 p-1 rounded transition-colors"
                          >
                            <Download className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(report.id)}
                            className="text-red-600 hover:text-red-900 p-1 rounded transition-colors"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}
