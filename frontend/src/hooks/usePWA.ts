import { useState, useEffect } from 'react';

interface PWAStatus {
  isOnline: boolean;
  isInstalled: boolean;
  canInstall: boolean;
  isStandalone: boolean;
}

export function usePWA() {
  const [pwaStatus, setPwaStatus] = useState<PWAStatus>({
    isOnline: true,
    isInstalled: false,
    canInstall: false,
    isStandalone: false,
  });

  useEffect(() => {
    // 온라인/오프라인 상태 확인
    const updateOnlineStatus = () => {
      setPwaStatus(prev => ({
        ...prev,
        isOnline: navigator.onLine,
      }));
    };

    // PWA 설치 상태 확인
    const checkInstallStatus = () => {
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
      const isInstalled = window.matchMedia('(display-mode: standalone)').matches || 
                         (window.navigator as any).standalone === true;

      setPwaStatus(prev => ({
        ...prev,
        isInstalled,
        isStandalone,
      }));
    };

    // 초기 상태 설정
    updateOnlineStatus();
    checkInstallStatus();

    // 이벤트 리스너 등록
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    window.addEventListener('focus', checkInstallStatus);

    return () => {
      window.removeEventListener('online', updateOnlineStatus);
      window.removeEventListener('offline', updateOnlineStatus);
      window.removeEventListener('focus', checkInstallStatus);
    };
  }, []);

  // 네트워크 상태 모니터링
  const checkNetworkStatus = async () => {
    try {
      const response = await fetch('/api/health', { 
        method: 'HEAD',
        cache: 'no-cache'
      });
      return response.ok;
    } catch {
      return false;
    }
  };

  // 캐시 상태 확인
  const getCacheStatus = async () => {
    if ('caches' in window) {
      try {
        const cacheNames = await caches.keys();
        const cacheDetails = await Promise.all(
          cacheNames.map(async (name) => {
            const cache = await caches.open(name);
            const keys = await cache.keys();
            return { name, size: keys.length };
          })
        );
        return cacheDetails;
      } catch (error) {
        console.error('캐시 상태 확인 실패:', error);
        return [];
      }
    }
    return [];
  };

  // 캐시 정리
  const clearCache = async () => {
    if ('caches' in window) {
      try {
        const cacheNames = await caches.keys();
        await Promise.all(
          cacheNames.map(name => caches.delete(name))
        );
        return true;
      } catch (error) {
        console.error('캐시 정리 실패:', error);
        return false;
      }
    }
    return false;
  };

  // 백그라운드 동기화 등록
  const registerBackgroundSync = async (tag: string) => {
    if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
      try {
        const registration = await navigator.serviceWorker.ready;
        await registration.sync.register(tag);
        return true;
      } catch (error) {
        console.error('백그라운드 동기화 등록 실패:', error);
        return false;
      }
    }
    return false;
  };

  // 푸시 알림 권한 요청
  const requestNotificationPermission = async () => {
    if ('Notification' in window) {
      try {
        const permission = await Notification.requestPermission();
        return permission;
      } catch (error) {
        console.error('알림 권한 요청 실패:', error);
        return 'denied';
      }
    }
    return 'unsupported';
  };

  // 앱 업데이트 확인
  const checkForUpdates = async () => {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.getRegistration();
        if (registration) {
          await registration.update();
          return true;
        }
      } catch (error) {
        console.error('업데이트 확인 실패:', error);
      }
    }
    return false;
  };

  return {
    ...pwaStatus,
    checkNetworkStatus,
    getCacheStatus,
    clearCache,
    registerBackgroundSync,
    requestNotificationPermission,
    checkForUpdates,
  };
}
