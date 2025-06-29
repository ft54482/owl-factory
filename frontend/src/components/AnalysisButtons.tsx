import React, { useState } from 'react';
import { Play, User, Loader2, Video, Users } from 'lucide-react';

interface AnalysisButtonsProps {
  disabled?: boolean;
  videoUrl?: string;
  onSingleVideoAnalysis?: () => void;
  onCompleteAccountAnalysis?: () => void;
}

export const AnalysisButtons: React.FC<AnalysisButtonsProps> = ({
  disabled = false,
  videoUrl,
  onSingleVideoAnalysis,
  onCompleteAccountAnalysis
}) => {
  const [loadingType, setLoadingType] = useState<'single' | 'complete' | null>(null);

  const handleSingleVideoClick = async () => {
    if (disabled || !videoUrl) return;
    
    setLoadingType('single');
    try {
      await onSingleVideoAnalysis?.();
    } finally {
      setLoadingType(null);
    }
  };

  const handleCompleteAccountClick = async () => {
    if (disabled || !videoUrl) return;
    
    setLoadingType('complete');
    try {
      await onCompleteAccountAnalysis?.();
    } finally {
      setLoadingType(null);
    }
  };

  const baseButtonClasses = `
    flex-1 px-4 py-2 sm:py-3 rounded-lg transition-all duration-200 
    flex items-center justify-center gap-2 text-sm sm:text-base font-medium
    disabled:opacity-50 disabled:cursor-not-allowed
    focus:outline-none focus:ring-2 focus:ring-offset-2
  `;

  const singleVideoClasses = `
    ${baseButtonClasses}
    bg-blue-600 text-white hover:bg-blue-700 active:bg-blue-800
    focus:ring-blue-500
    ${loadingType === 'single' ? 'bg-blue-700' : ''}
  `;

  const completeAccountClasses = `
    ${baseButtonClasses}
    bg-gradient-to-r from-purple-600 to-indigo-600 text-white 
    hover:from-purple-700 hover:to-indigo-700 active:from-purple-800 active:to-indigo-800
    focus:ring-purple-500 shadow-lg hover:shadow-xl
    ${loadingType === 'complete' ? 'from-purple-700 to-indigo-700' : ''}
  `;

  return (
    <div className="w-full space-y-3">
      {/* 按钮组容器 */}
      <div className="flex flex-col sm:flex-row gap-3 w-full">
        {/* 单视频分析按钮 */}
        <button
          onClick={handleSingleVideoClick}
          disabled={disabled || !videoUrl || loadingType !== null}
          className={singleVideoClasses}
          title="分析当前选中的单个视频内容"
        >
          {loadingType === 'single' ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>分析中...</span>
            </>
          ) : (
            <>
              <Video className="w-4 h-4" />
              <span>单视频分析</span>
            </>
          )}
        </button>

        {/* 完整账号分析按钮 */}
        <button
          onClick={handleCompleteAccountClick}
          disabled={disabled || !videoUrl || loadingType !== null}
          className={completeAccountClasses}
          title="分析该账号的所有公开视频内容"
        >
          {loadingType === 'complete' ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>分析中...</span>
            </>
          ) : (
            <>
              <Users className="w-4 h-4" />
              <span>完整账号分析</span>
            </>
          )}
        </button>
      </div>

      {/* 功能说明文字 */}
      <div className="text-xs text-gray-500 space-y-1">
        <div className="flex items-center gap-2">
          <Video className="w-3 h-3 text-blue-500" />
          <span>单视频分析：快速分析当前视频的语音转录和内容洞察</span>
        </div>
        <div className="flex items-center gap-2">
          <Users className="w-3 h-3 text-purple-500" />
          <span>完整账号分析：深度分析该账号所有视频，生成综合报告</span>
        </div>
      </div>

      {/* 状态提示 */}
      {loadingType && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-sm text-blue-700">
          <div className="flex items-center gap-2">
            <Loader2 className="w-4 h-4 animate-spin" />
            <span>
              {loadingType === 'single' 
                ? '正在调用MoreAPI获取视频链接，并分发到GPU集群进行转录分析...' 
                : '正在批量获取账号视频，这可能需要几分钟时间，请耐心等待...'}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisButtons;