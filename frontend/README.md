# Est Mate Frontend

Next.js 기반의 지속가능성 보고서 작성 PWA 플랫폼

## 🚀 기술 스택

- **Framework**: Next.js 14
- **Language**: TypeScript
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Styling**: Tailwind CSS
- **PWA**: Next.js PWA
- **Package Manager**: pnpm

## 🏗️ 프로젝트 구조

```
src/
├── app/                 # Next.js App Router
├── components/          # 재사용 가능한 컴포넌트
├── domain/             # 도메인별 페이지
├── services/           # API 서비스
├── store/              # Zustand 스토어
└── types/              # TypeScript 타입 정의
```

## 🛠️ 개발 환경 설정

### 필수 요구사항

- Node.js 18.x 이상
- pnpm 8.x 이상

### 설치 및 실행

```bash
# 의존성 설치
pnpm install

# 개발 서버 실행
pnpm dev

# 프로덕션 빌드
pnpm build

# 프로덕션 서버 실행
pnpm start
```

## 🧪 테스트

```bash
# 단위 테스트 실행
pnpm test

# 테스트 커버리지 확인
pnpm test:coverage

# E2E 테스트 실행
pnpm test:e2e

# 테스트 감시 모드
pnpm test:watch
```

## 📝 코드 품질

```bash
# 린팅
pnpm lint

# 린팅 자동 수정
pnpm lint:fix

# 타입 체크
pnpm type-check

# 코드 포맷팅
pnpm format

# 포맷팅 검사
pnpm format:check
```

## 🔄 CI/CD 파이프라인

### GitHub Actions 워크플로우

1. **Quality Check**: 코드 품질, 린팅, 타입 체크, 빌드, 테스트
2. **Security Scan**: 보안 취약점 스캔
3. **Deploy Preview**: develop 브랜치 → Vercel Preview
4. **Deploy Production**: main 브랜치 → Vercel Production
5. **Performance Test**: Lighthouse CI를 통한 성능 테스트
6. **Notification**: 배포 상태 알림

### 브랜치 전략

- **main**: 프로덕션 배포
- **develop**: 프리뷰 배포 및 테스트

### 자동화된 작업

- 코드 품질 검사
- 자동 테스트 실행
- 보안 스캔
- 성능 테스트
- 자동 배포
- 알림 발송

## 🔐 환경변수

프로젝트 루트에 `.env.local` 파일을 생성하고 다음 변수들을 설정하세요:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_APP_URL=https://app.example.com

# Authentication
NEXT_PUBLIC_AUTH_DOMAIN=auth.example.com
NEXT_PUBLIC_AUTH_CLIENT_ID=your_client_id

# External Services
MATERIALITY_SERVICE_URL=https://materiality-service.example.com
SURVEY_SERVICE_URL=https://survey-service.example.com
AUTH_SERVICE_URL=https://auth-service.example.com

# CORS
CORS_ORIGINS=https://app.example.com,https://localhost:3000
```

## 🚀 배포

### Vercel 배포

1. Vercel 프로젝트 연결
2. 환경변수 설정
3. GitHub Actions를 통한 자동 배포

### 수동 배포

```bash
# 프로덕션 빌드
pnpm build

# Vercel 배포
vercel --prod
```

## 📱 PWA 기능

- 오프라인 지원
- 홈 화면 설치
- 푸시 알림
- 백그라운드 동기화

## 🔧 개발 도구

- **ESLint**: 코드 품질 검사
- **Prettier**: 코드 포맷팅
- **Husky**: Git 훅
- **lint-staged**: 커밋 전 자동 검사
- **Jest**: 단위 테스트
- **Playwright**: E2E 테스트
- **Lighthouse CI**: 성능 테스트

## 📊 모니터링

- Vercel Analytics
- Lighthouse CI 성능 지표
- GitHub Actions 실행 상태
- 보안 취약점 스캔 결과

## 🤝 기여 가이드

1. Fork 및 Clone
2. Feature 브랜치 생성
3. 코드 작성 및 테스트
4. Pull Request 생성
5. 코드 리뷰 후 머지

## 📄 라이선스

MIT License

## 🆘 지원

문제가 발생하거나 질문이 있으시면 GitHub Issues를 통해 문의해주세요.
