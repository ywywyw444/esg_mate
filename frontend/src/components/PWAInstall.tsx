'use client';

import React, { useState, useEffect } from 'react';

interface BeforeInstallPromptEvent extends Event {
  readonly platforms: string[];
  readonly userChoice: Promise<{
    outcome: 'accepted' | 'dismissed';
    platform: string;
  }>;
  prompt(): Promise<void>;
}

export default function PWAInstall() {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);
  const [showInstallButton, setShowInstallButton] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);

  useEffect(() => {
    // PWA 설치 가능 여부 확인
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
      setShowInstallButton(true);
    };

    // PWA 설치 완료 확인
    const handleAppInstalled = () => {
      setIsInstalled(true);
      setShowInstallButton(false);
      console.log('PWA가 성공적으로 설치되었습니다!');
    };

    // 이미 설치되어 있는지 확인
    if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
    }

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) return;

    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;

    if (outcome === 'accepted') {
      console.log('사용자가 PWA 설치를 수락했습니다');
    } else {
      console.log('사용자가 PWA 설치를 거부했습니다');
    }

    setDeferredPrompt(null);
    setShowInstallButton(false);
  };

  const handleShareClick = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: 'Est Mate - 지속가능성 보고서 작성 도구',
          text: 'GRI, TCFD 등 지속가능성 보고서 작성을 위한 종합 플랫폼',
          url: window.location.href,
        });
      } catch (error) {
        console.log('공유가 취소되었습니다');
      }
    } else {
      // 공유 API를 지원하지 않는 경우 URL 복사
      navigator.clipboard.writeText(window.location.href);
      alert('URL이 클립보드에 복사되었습니다!');
    }
  };

  if (isInstalled) {
    return (
      <div className="fixed bottom-4 right-4 bg-green-100 border border-green-300 rounded-lg p-3 shadow-lg">
        <div className="flex items-center text-green-800 text-sm">
          <span className="mr-2">✅</span>
          <span>앱이 설치되었습니다</span>
        </div>
      </div>
    );
  }

  if (!showInstallButton) {
    return null;
  }

  return (
    <div className="fixed bottom-4 right-4 bg-white border border-gray-300 rounded-lg p-4 shadow-lg max-w-sm">
      <div className="flex items-start space-x-3">
        <div className="flex-shrink-0">
          <div className="w-10 h-10 bg-gradient-to-r from-teal-500 to-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white text-lg">📱</span>
          </div>
        </div>
        
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-medium text-gray-900 mb-1">
            Est Mate 앱 설치
          </h3>
          <p className="text-xs text-gray-500 mb-3">
            홈 화면에 추가하여 더 빠르게 접근하세요
          </p>
          
          <div className="flex space-x-2">
            <button
              onClick={handleInstallClick}
              className="flex-1 bg-gradient-to-r from-teal-500 to-blue-600 text-white text-xs font-medium py-2 px-3 rounded-md hover:from-teal-600 hover:to-blue-700 transition-all duration-200"
            >
              설치하기
            </button>
            
            <button
              onClick={handleShareClick}
              className="flex-1 bg-gray-100 text-gray-700 text-xs font-medium py-2 px-3 rounded-md hover:bg-gray-200 transition-all duration-200"
            >
              공유하기
            </button>
          </div>
        </div>
        
        <button
          onClick={() => setShowInstallButton(false)}
          className="flex-shrink-0 text-gray-400 hover:text-gray-600"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
}
