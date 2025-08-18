// workbox 타입 정의
interface Workbox {
  messageSkipWaiting?: () => void;
  messageSW?: (message: any) => void;
}

// Window 인터페이스 확장
declare global {
  interface Window {
    workbox?: unknown;
  }
}

// Service Worker 등록
export function register() {
  if (
    typeof window !== 'undefined' &&
    'serviceWorker' in navigator &&
    !('workbox' in window)
  ) {
    const swUrl = '/sw.js';

    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register(swUrl)
        .then((registration) => {
          console.log('SW registered: ', registration);

          // 업데이트 확인
          registration.addEventListener('updatefound', () => {
            const newWorker = registration.installing;
            if (newWorker) {
              newWorker.addEventListener('statechange', () => {
                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                  // 새로운 SW가 설치되었을 때 사용자에게 알림
                  if (confirm('새로운 버전이 사용 가능합니다. 새로고침하시겠습니까?')) {
                    window.location.reload();
                  }
                }
              });
            }
          });
        })
        .catch((registrationError) => {
          console.log('SW registration failed: ', registrationError);
        });
    });

    // SW 업데이트 체크
    let refreshing = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (refreshing) return;
      refreshing = true;
      window.location.reload();
    });
  }
}

// Service Worker 등록 해제
export function unregister() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready
      .then((registration) => {
        registration.unregister();
      })
      .catch((error) => {
        console.error(error.message);
      });
  }
}
