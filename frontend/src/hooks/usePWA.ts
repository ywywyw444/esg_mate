import { useState, useEffect } from 'react';

interface PWAStatus {
  isOnline: boolean;
  isInstalled: boolean;
  canInstall: boolean;
  isStandalone: boolean;
}

// ServiceWorkerRegistration에 sync 속성 추가를 위한 타입 확장
interface ExtendedServiceWorkerRegistration extends ServiceWorkerRegistration {
  sync?: {
    register(tag: string): Promise<void>;
  };
}

// Navigator 인터페이스 확장
interface ExtendedNavigator extends Navigator {
  standalone?: boolean;
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
    const updateOnlineStatus = async () => {
      setPwaStatus(prev => ({
        ...prev,
        isOnline: navigator.onLine,
      }));
    };

    // PWA 설치 상태 확인
    const checkInstallStatus = async () => {
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
      const extendedNavigator = navigator as ExtendedNavigator;
      const isInstalled = window.matchMedia('(display-mode: standalone)').matches || 
                         extendedNavigator.standalone === true;

      setPwaStatus(prev => ({
        ...prev,
        isInstalled,
        isStandalone,
      }));
    };

    // 초기 상태 설정
    const initializeStatus = async () => {
      await Promise.all([
        updateOnlineStatus(),
        checkInstallStatus()
      ]);
    };

    initializeStatus();

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
  const checkNetworkStatus = async (): Promise<boolean> => {
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
  const getCacheStatus = async (): Promise<Array<{ name: string; size: number }>> => {
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
  const clearCache = async (): Promise<boolean> => {
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
  const registerBackgroundSync = async (tag: string): Promise<boolean> => {
    if ('serviceWorker' in navigator) {
      try {
        const registration = await navigator.serviceWorker.ready;
        const extendedRegistration = registration as ExtendedServiceWorkerRegistration;
        
        // sync 속성이 존재하는지 확인
        if (extendedRegistration.sync && typeof extendedRegistration.sync.register === 'function') {
          await extendedRegistration.sync.register(tag);
          return true;
        } else {
          console.warn('백그라운드 동기화가 지원되지 않습니다.');
          return false;
        }
      } catch (error) {
        console.error('백그라운드 동기화 등록 실패:', error);
        return false;
      }
    }
    return false;
  };

  // 푸시 알림 권한 요청
  const requestNotificationPermission = async (): Promise<NotificationPermission | 'unsupported'> => {
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
  const checkForUpdates = async (): Promise<boolean> => {
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

  // PWA 설치 가능 여부 확인
  const checkInstallability = async (): Promise<boolean> => {
    try {
      // beforeinstallprompt 이벤트가 발생했는지 확인
      return new Promise((resolve) => {
        const checkPrompt = () => {
          // PWA 설치 조건 확인
          const hasValidManifest = !!document.querySelector('link[rel="manifest"]');
          const hasServiceWorker = 'serviceWorker' in navigator;
          const isHttps = location.protocol === 'https:' || location.hostname === 'localhost';
          
          resolve(hasValidManifest && hasServiceWorker && isHttps);
        };

        // 즉시 확인
        checkPrompt();
        
        // 이벤트 리스너 등록
        const handleBeforeInstallPrompt = () => resolve(true);
        window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
        
        // 1초 후 타임아웃
        setTimeout(() => {
          window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
          resolve(false);
        }, 1000);
      });
    } catch (error) {
      console.error('설치 가능 여부 확인 실패:', error);
      return false;
    }
  };

  // PWA 설치 상태 모니터링
  const monitorInstallStatus = async (): Promise<void> => {
    try {
      const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
      const extendedNavigator = navigator as ExtendedNavigator;
      const isInstalled = isStandalone || extendedNavigator.standalone === true;
      
      setPwaStatus(prev => ({
        ...prev,
        isInstalled,
        isStandalone,
      }));

      // 설치 가능 여부도 확인
      const canInstall = await checkInstallability();
      setPwaStatus(prev => ({
        ...prev,
        canInstall,
      }));
    } catch (error) {
      console.error('설치 상태 모니터링 실패:', error);
    }
  };

  return {
    ...pwaStatus,
    checkNetworkStatus,
    getCacheStatus,
    clearCache,
    registerBackgroundSync,
    requestNotificationPermission,
    checkForUpdates,
    checkInstallability,
    monitorInstallStatus,
  };
}
