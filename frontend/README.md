# Est Mate - 지속가능성 보고서 작성 PWA

GRI, TCFD 등 지속가능성 보고서 작성을 위한 종합 Progressive Web App (PWA) 플랫폼입니다.

## 🚀 주요 기능

- **GRI 보고서 작성**: GRI 표준에 따른 지속가능성 보고서 작성 도구
- **TCFD 보고서 작성**: 기후 관련 재무정보 공시 보고서 작성 도구
- **중대성 평가**: ESG 요소별 중대성 평가 및 관리
- **PWA 지원**: 모바일 앱과 같은 사용자 경험
- **오프라인 지원**: 네트워크 연결 없이도 기본 기능 사용 가능

## 🛠️ 기술 스택

- **Frontend**: Next.js 15, React 19, TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **PWA**: Service Worker, Web App Manifest
- **Deployment**: Vercel

## 📱 PWA 기능

### 설치 및 사용
- 홈 화면에 앱 추가 가능
- 독립 실행 모드 지원
- 네이티브 앱과 유사한 사용자 경험

### 오프라인 지원
- Service Worker를 통한 캐싱
- 오프라인 상태에서도 기본 기능 사용
- 자동 동기화 및 업데이트

### 성능 최적화
- 자동 캐싱 및 업데이트
- 백그라운드 동기화
- 푸시 알림 지원

## 🚀 시작하기

### 필수 요구사항
- Node.js 20.x
- npm 10.x

### 설치
```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev

# 프로덕션 빌드
npm run build

# 프로덕션 서버 실행
npm start
```

### PWA 관련 명령어
```bash
# PWA 빌드
npm run pwa:build

# PWA 분석
npm run pwa:analyze

# PWA 테스트
npm run pwa:test
```

## 📁 프로젝트 구조

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (domain)/          # 도메인별 페이지
│   │   │   ├── auth/          # 인증 관련
│   │   │   ├── gri/           # GRI 보고서
│   │   │   └── tcfd/          # TCFD 보고서
│   │   ├── dashboard/         # 대시보드
│   │   └── layout.tsx         # 루트 레이아웃
│   ├── components/             # 재사용 가능한 컴포넌트
│   │   ├── PWAInstall.tsx     # PWA 설치 컴포넌트
│   │   └── PWAStatus.tsx      # PWA 상태 표시
│   ├── hooks/                  # 커스텀 훅
│   │   └── usePWA.ts          # PWA 관련 훅
│   └── store/                  # 상태 관리
├── public/                     # 정적 파일
│   ├── manifest.json           # PWA 매니페스트
│   ├── sw.js                   # Service Worker
│   ├── offline.html            # 오프라인 페이지
│   └── icons/                  # PWA 아이콘
└── package.json
```

## 🔧 PWA 설정

### 매니페스트 파일
- `public/manifest.json`: PWA 기본 설정
- 앱 이름, 아이콘, 테마 색상 등 정의

### Service Worker
- `public/sw.js`: 오프라인 지원 및 캐싱
- 자동 업데이트 및 백그라운드 동기화

### 메타 태그
- `src/app/layout.tsx`: PWA 관련 메타 태그
- iOS 및 Android 최적화

## 📱 모바일 최적화

### 반응형 디자인
- 모든 화면 크기 지원
- 터치 친화적 인터페이스
- 모바일 우선 설계

### 성능 최적화
- 이미지 최적화
- 코드 스플리팅
- 지연 로딩

## 🚀 배포

### Vercel 배포
```bash
# Vercel CLI 설치
npm i -g vercel

# 배포
vercel --prod
```

### 환경 변수
```bash
# .env.local
NEXT_PUBLIC_API_URL=your_api_url
NEXT_PUBLIC_PWA_ENABLED=true
```

## 📊 성능 모니터링

### Core Web Vitals
- LCP (Largest Contentful Paint)
- FID (First Input Delay)
- CLS (Cumulative Layout Shift)

### PWA 메트릭
- 설치율
- 오프라인 사용률
- 캐시 히트율

## 🔍 개발 도구

### PWA 디버깅
- Chrome DevTools > Application > Service Workers
- Lighthouse PWA 감사
- Chrome DevTools > Application > Manifest

### 테스트
```bash
# PWA 테스트
npm run pwa:test

# 성능 분석
npm run pwa:analyze
```

## 📚 참고 자료

- [PWA 가이드](https://web.dev/progressive-web-apps/)
- [Service Worker API](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API)
- [Web App Manifest](https://developer.mozilla.org/en-US/docs/Web/Manifest)
- [Next.js PWA](https://nextjs.org/docs/app/building-your-application/optimizing/progressive-web-apps)

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.

---

**Est Mate** - 지속가능한 미래를 위한 보고서 작성 도구 🚀
