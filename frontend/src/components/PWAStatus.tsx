'use client';

import React from 'react';
import { usePWA } from '@/hooks/usePWA';

export default function PWAStatus() {
  const { 
    isOnline, 
    isInstalled, 
    isStandalone,
    checkNetworkStatus,
    getCacheStatus,
    clearCache,
    checkForUpdates 
  } = usePWA();

  const [cacheInfo, setCacheInfo] = React.useState<any[]>([]);
  const [isChecking, setIsChecking] = React.useState(false);

  const handleCheckCache = async () => {
    setIsChecking(true);
    try {
      const cacheStatus = await getCacheStatus();
      setCacheInfo(cacheStatus);
    } catch (error) {
      console.error('캐시 상태 확인 실패:', error);
    } finally {
      setIsChecking(false);
    }
  };

  const handleClearCache = async () => {
    if (confirm('모든 캐시를 정리하시겠습니까?')) {
      try {
        const success = await clearCache();
        if (success) {
          alert('캐시가 성공적으로 정리되었습니다.');
          setCacheInfo([]);
        } else {
          alert('캐시 정리에 실패했습니다.');
        }
      } catch (error) {
        console.error('캐시 정리 실패:', error);
        alert('캐시 정리 중 오류가 발생했습니다.');
      }
    }
  };

  const handleCheckUpdates = async () => {
    try {
      const hasUpdates = await checkForUpdates();
      if (hasUpdates) {
        alert('업데이트 확인이 완료되었습니다.');
      } else {
        alert('현재 최신 버전입니다.');
      }
    } catch (error) {
      console.error('업데이트 확인 실패:', error);
      alert('업데이트 확인에 실패했습니다.');
    }
  };

  return (
    <div className="fixed top-4 left-4 bg-white border border-gray-300 rounded-lg p-4 shadow-lg max-w-sm z-50">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-medium text-gray-900">PWA 상태</h3>
        <div className="flex space-x-2">
          <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'}`} 
               title={isOnline ? '온라인' : '오프라인'} />
          <div className={`w-2 h-2 rounded-full ${isInstalled ? 'bg-blue-500' : 'bg-gray-400'}`} 
               title={isInstalled ? '설치됨' : '설치되지 않음'} />
        </div>
      </div>

      <div className="space-y-2 text-xs text-gray-600">
        <div className="flex justify-between">
          <span>네트워크:</span>
          <span className={isOnline ? 'text-green-600' : 'text-red-600'}>
            {isOnline ? '온라인' : '오프라인'}
          </span>
        </div>
        
        <div className="flex justify-between">
          <span>설치 상태:</span>
          <span className={isInstalled ? 'text-blue-600' : 'text-gray-600'}>
            {isInstalled ? '설치됨' : '설치되지 않음'}
          </span>
        </div>
        
        <div className="flex justify-between">
          <span>독립 실행:</span>
          <span className={isStandalone ? 'text-green-600' : 'text-gray-600'}>
            {isStandalone ? '예' : '아니오'}
          </span>
        </div>
      </div>

      <div className="mt-3 space-y-2">
        <button
          onClick={handleCheckCache}
          disabled={isChecking}
          className="w-full bg-gray-100 text-gray-700 text-xs py-2 px-3 rounded hover:bg-gray-200 transition-colors disabled:opacity-50"
        >
          {isChecking ? '확인 중...' : '캐시 상태 확인'}
        </button>
        
        {cacheInfo.length > 0 && (
          <div className="bg-gray-50 p-2 rounded text-xs">
            <div className="font-medium mb-1">캐시 정보:</div>
            {cacheInfo.map((cache, index) => (
              <div key={index} className="text-gray-600">
                {cache.name}: {cache.size}개 파일
              </div>
            ))}
          </div>
        )}
        
        <div className="flex space-x-2">
          <button
            onClick={handleClearCache}
            className="flex-1 bg-red-100 text-red-700 text-xs py-2 px-3 rounded hover:bg-red-200 transition-colors"
          >
            캐시 정리
          </button>
          
          <button
            onClick={handleCheckUpdates}
            className="flex-1 bg-blue-100 text-blue-700 text-xs py-2 px-3 rounded hover:bg-blue-200 transition-colors"
          >
            업데이트 확인
          </button>
        </div>
      </div>
    </div>
  );
}
