'use client';

import { useEffect } from 'react';

export default function SWRegister() {
  useEffect(() => {
    if (
      typeof window !== 'undefined' &&
      'serviceWorker' in navigator &&
      window.workbox === undefined
    ) {
      const swUrl = '/sw.js';

      navigator.serviceWorker
        .register(swUrl)
        .then((registration) => {
          console.log('Service Worker 등록 성공:', registration);

          // 업데이트 확인
          registration.addEventListener('updatefound', () => {
            const newWorker = registration.installing;
            if (newWorker) {
              newWorker.addEventListener('statechange', () => {
                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                  // 새로운 Service Worker가 설치되었을 때 사용자에게 알림
                  if (confirm('새로운 버전이 사용 가능합니다. 업데이트하시겠습니까?')) {
                    newWorker.postMessage({ type: 'SKIP_WAITING' });
                    window.location.reload();
                  }
                }
              });
            }
          });

          // Service Worker가 제어권을 가졌을 때
          if (navigator.serviceWorker.controller) {
            console.log('Service Worker가 페이지를 제어하고 있습니다');
          }
        })
        .catch((error) => {
          console.error('Service Worker 등록 실패:', error);
        });

      // Service Worker 메시지 수신
      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data && event.data.type === 'RELOAD_PAGE') {
          window.location.reload();
        }
      });
    }
  }, []);

  return null;
}
