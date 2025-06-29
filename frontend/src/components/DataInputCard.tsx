import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link, Zap, Plus, X, FileText, Users, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAppStore } from '@/store';
import analysisService from '@/services/analysisService';

interface UrlItem {
  id: string;
  url: string;
  platform: string;
  isValid: boolean;
  type: 'video' | 'profile' | 'unknown';
}

export default function DataInputCard() {
  const navigate = useNavigate();
  const { addTask } = useAppStore();
  const [urls, setUrls] = useState<UrlItem[]>([
    { id: '1', url: '', platform: '', isValid: false, type: 'unknown' }
  ]);
  const [isProcessing, setIsProcessing] = useState(false);

  const validateUrl = (input: string) => {
    if (!input.trim()) return false;
    
    // 支持抖音、小红书、B站等平台的URL格式
    const platformPatterns = [
      // 抖音视频链接
      /^https?:\/\/(www\.)?douyin\.com\/video\/\d+/,
      /^https?:\/\/(www\.)?iesdouyin\.com\/share\/video\/\d+/,
      /^https?:\/\/v\.douyin\.com\/[A-Za-z0-9]+/,
      // 抖音用户主页
      /^https?:\/\/(www\.)?douyin\.com\/user\/[A-Za-z0-9_-]+/,
      // 小红书
      /^https?:\/\/(www\.)?xiaohongshu\.com\/(explore\/|user\/profile\/|discovery\/item\/)/,
      /^https?:\/\/xhslink\.com\/[A-Za-z0-9]+/,
      // B站
      /^https?:\/\/(www\.)?bilibili\.com\/(video\/|space\/)/,
      // 通用URL检查
      /^https?:\/\/[^\s<>"{}|\\^`[\]]+$/
    ];
    
    return platformPatterns.some(pattern => pattern.test(input));
  };

  const detectPlatform = (url: string) => {
    if (url.includes('douyin.com') || url.includes('iesdouyin.com') || url.includes('v.douyin.com')) {
      return '抖音';
    }
    if (url.includes('xiaohongshu.com') || url.includes('xhslink.com')) {
      return '小红书';
    }
    if (url.includes('bilibili.com')) {
      return 'B站';
    }
    if (url.includes('tiktok.com')) {
      return 'TikTok';
    }
    return '其他平台';
  };

  const detectUrlType = (url: string): 'video' | 'profile' | 'unknown' => {
    // 检测是否为视频链接
    if (url.includes('/video/') || url.includes('/share/video/') || 
        url.includes('v.douyin.com') || url.includes('/discovery/item/') ||
        url.includes('xhslink.com')) {
      return 'video';
    }
    
    // 检测是否为用户主页
    if (url.includes('/user/') || url.includes('/space/') || 
        url.includes('/user/profile/')) {
      return 'profile';
    }
    
    return 'unknown';
  };

  const handleUrlChange = (id: string, value: string) => {
    setUrls(urls.map(item => 
      item.id === id 
        ? { 
            ...item, 
            url: value, 
            platform: detectPlatform(value),
            isValid: validateUrl(value),
            type: detectUrlType(value)
          }
        : item
    ));
  };

  const addUrl = () => {
    const newId = Date.now().toString();
    setUrls([...urls, { id: newId, url: '', platform: '', isValid: false, type: 'unknown' }]);
  };

  const removeUrl = (id: string) => {
    if (urls.length > 1) {
      setUrls(urls.filter(item => item.id !== id));
    }
  };

  const clearAll = () => {
    setUrls([{ id: '1', url: '', platform: '', isValid: false, type: 'unknown' }]);
  };

  const handleSingleVideoAnalysis = async () => {
    const validUrls = urls.filter(item => item.isValid && item.url.trim());
    if (validUrls.length === 0) return;
    
    setIsProcessing(true);
    try {
      const selectedUrl = validUrls[0];
      
      // 创建新任务
      const newTask = addTask(selectedUrl.url, 'default'); // 使用默认模板
      
      // 导航到分析页面
      navigate(`/analysis/${newTask.id}`);
      
      // 开始分析
      await analysisService.startAnalysis({
        url: selectedUrl.url,
        templateId: 'default',
        analysisType: 'single'
      });
      
    } catch (error) {
      console.error('单视频分析失败:', error);
      // 可以在这里添加错误提示
    } finally {
      setIsProcessing(false);
    }
  };

  const handleFullAccountAnalysis = async () => {
    const validUrls = urls.filter(item => item.isValid && item.url.trim());
    if (validUrls.length === 0) return;
    
    setIsProcessing(true);
    try {
      // 处理批量URL
      for (const urlItem of validUrls) {
        // 创建新任务
        const newTask = addTask(urlItem.url, 'default');
        
        // 开始分析
        await analysisService.startAnalysis({
          url: urlItem.url,
          templateId: 'default',
          analysisType: urlItem.type === 'profile' ? 'complete' : 'single'
        });
      }
      
      // 导航到控制台查看所有任务
      navigate('/dashboard');
      
    } catch (error) {
      console.error('完整账号分析失败:', error);
      // 可以在这里添加错误提示
    } finally {
      setIsProcessing(false);
    }
  };

  const validUrlCount = urls.filter(item => item.isValid && item.url.trim()).length;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="bg-white rounded-xl shadow-lg p-6"
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <motion.div 
            whileHover={{ rotate: 10, scale: 1.1 }}
            className="p-3 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl shadow-lg"
          >
            <Zap className="w-6 h-6 text-white" />
          </motion.div>
          <div>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              智能批量分析
            </h2>
            <p className="text-sm text-gray-500 mt-1">
              AI驱动的多平台视频内容分析系统
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <motion.button
            onClick={addUrl}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="p-3 text-blue-600 hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50 rounded-xl transition-all duration-200 border border-blue-200 hover:border-blue-300"
          >
            <Plus className="w-5 h-5" />
          </motion.button>
        </div>
      </div>

      <div className="space-y-3 mb-4">
        {urls.map((item, index) => (
          <div key={item.id} className="relative">
            <div className="flex items-center space-x-2">
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={item.url}
                  onChange={(e) => handleUrlChange(item.id, e.target.value)}
                  placeholder={`输入视频链接或账号主页...`}
                  className={`w-full px-4 py-3 pl-10 border rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                    item.url && !item.isValid ? 'border-red-300 bg-red-50' : 
                    item.isValid ? 'border-green-300 bg-green-50' : 'border-gray-200'
                  }`}
                />
                <Link className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              </div>
              {urls.length > 1 && (
                <button
                  onClick={() => removeUrl(item.id)}
                  className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>
            
            {/* 平台标签 */}
            <AnimatePresence>
              {item.platform && item.isValid && (
                <motion.div 
                  initial={{ opacity: 0, y: -10, scale: 0.9 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -10, scale: 0.9 }}
                  transition={{ duration: 0.2 }}
                  className="flex items-center gap-2 mt-2 ml-10"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-500">已识别平台：</span>
                    <div className={`inline-flex items-center px-3 py-1.5 rounded-full text-xs font-medium ${
                      item.platform === '抖音' ? 'bg-gradient-to-r from-red-500 to-pink-500 text-white shadow-lg shadow-red-200' :
                      item.platform === '小红书' ? 'bg-gradient-to-r from-pink-500 to-rose-500 text-white shadow-lg shadow-pink-200' :
                      item.platform === 'B站' ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg shadow-blue-200' :
                      'bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-lg shadow-green-200'
                    }`}>
                      {item.platform}
                    </div>
                    <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs ${
                      item.type === 'video' ? 'bg-blue-100 text-blue-700' :
                      item.type === 'profile' ? 'bg-purple-100 text-purple-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {item.type === 'video' ? '视频' : item.type === 'profile' ? '主页' : '未知'}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>

      {/* 操作按钮区域 */}
      <div className="flex flex-col sm:flex-row gap-3">
        <motion.button
          onClick={handleSingleVideoAnalysis}
          disabled={validUrlCount === 0 || isProcessing}
          whileHover={{ scale: validUrlCount > 0 ? 1.02 : 1 }}
          whileTap={{ scale: validUrlCount > 0 ? 0.98 : 1 }}
          className="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-3 rounded-xl font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed hover:from-blue-700 hover:to-blue-800 shadow-lg hover:shadow-xl"
        >
          <div className="flex items-center justify-center gap-2">
            {isProcessing ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <FileText className="w-5 h-5" />
            )}
            <span>单视频分析</span>
          </div>
        </motion.button>

        <motion.button
          onClick={handleFullAccountAnalysis}
          disabled={validUrlCount === 0 || isProcessing}
          whileHover={{ scale: validUrlCount > 0 ? 1.02 : 1 }}
          whileTap={{ scale: validUrlCount > 0 ? 0.98 : 1 }}
          className="flex-1 bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-6 py-3 rounded-xl font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed hover:from-purple-700 hover:to-indigo-700 shadow-lg hover:shadow-xl"
        >
          <div className="flex items-center justify-center gap-2">
            {isProcessing ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Users className="w-5 h-5" />
            )}
            <span>完整账号分析</span>
          </div>
        </motion.button>
      </div>

      {/* 状态信息 */}
      <div className="mt-4 text-sm text-gray-500">
        <div className="flex items-center justify-between">
          <span>已添加 {validUrlCount} 个有效链接</span>
          {urls.length > 1 && (
            <button
              onClick={clearAll}
              className="text-red-500 hover:text-red-700 transition-colors"
            >
              清空所有
            </button>
          )}
        </div>
      </div>
    </motion.div>
  );
}