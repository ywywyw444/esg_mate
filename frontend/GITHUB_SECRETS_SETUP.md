# GitHub Secrets 설정 가이드

CI/CD 파이프라인이 정상적으로 작동하려면 다음 GitHub Secrets를 설정해야 합니다.

## 🔐 필수 Secrets

### Vercel 관련

1. **VERCEL_TOKEN**
   - Vercel 대시보드 → Settings → Tokens
   - "Create" 클릭하여 새 토큰 생성
   - 토큰을 복사하여 GitHub Secrets에 저장

2. **VERCEL_ORG_ID**
   - Vercel 대시보드 → Settings → General
   - "Organization ID" 값 복사
   - GitHub Secrets에 저장

3. **VERCEL_PROJECT_ID**
   - Vercel 프로젝트 페이지 → Settings → General
   - "Project ID" 값 복사
   - GitHub Secrets에 저장

### 성능 테스트 관련

4. **LHCI_GITHUB_APP_TOKEN**
   - [Lighthouse CI GitHub App](https://github.com/apps/lighthouse-ci) 설치
   - 토큰 생성 및 GitHub Secrets에 저장

### 알림 관련 (선택사항)

5. **SLACK_WEBHOOK_URL**
   - Slack 워크스페이스에서 Incoming Webhook 생성
   - Webhook URL을 GitHub Secrets에 저장

## 📋 설정 방법

### 1. GitHub Repository 설정

1. GitHub 저장소로 이동
2. Settings → Secrets and variables → Actions
3. "New repository secret" 클릭

### 2. 각 Secret 추가

```
Name: VERCEL_TOKEN
Value: [Vercel에서 생성한 토큰]

Name: VERCEL_ORG_ID
Value: [Vercel 조직 ID]

Name: VERCEL_PROJECT_ID
Value: [Vercel 프로젝트 ID]

Name: LHCI_GITHUB_APP_TOKEN
Value: [Lighthouse CI GitHub App 토큰]

Name: SLACK_WEBHOOK_URL
Value: [Slack Webhook URL]
```

## 🔍 Vercel 정보 찾는 방법

### Vercel Token 생성

1. [Vercel 대시보드](https://vercel.com/dashboard) 로그인
2. 우측 상단 프로필 → Settings
3. 좌측 메뉴 → Tokens
4. "Create" 클릭
5. 토큰 이름 입력 (예: "GitHub Actions")
6. "Create" 클릭하여 토큰 생성
7. 생성된 토큰 복사 (한 번만 표시됨)

### Organization ID 찾기

1. Vercel 대시보드 → Settings
2. "General" 탭
3. "Organization ID" 섹션에서 ID 복사

### Project ID 찾기

1. 해당 Vercel 프로젝트로 이동
2. Settings → General
3. "Project ID" 섹션에서 ID 복사

## 🚀 Lighthouse CI 설정

### 1. GitHub App 설치

1. [Lighthouse CI GitHub App](https://github.com/apps/lighthouse-ci) 방문
2. "Install" 클릭
3. 저장소 선택 후 설치

### 2. 토큰 생성

1. 설치된 App의 설정 페이지로 이동
2. "Generate token" 클릭
3. 생성된 토큰을 `LHCI_GITHUB_APP_TOKEN`으로 저장

## 📱 Slack 알림 설정 (선택사항)

### 1. Incoming Webhook 생성

1. Slack 워크스페이스에서 앱 추가
2. "Incoming Webhooks" 검색 및 설치
3. "Add to Slack" 클릭
4. 채널 선택 후 "Add Incoming WebHooks integration" 클릭
5. Webhook URL 복사

### 2. GitHub Secrets에 저장

복사한 Webhook URL을 `SLACK_WEBHOOK_URL`로 저장

## ✅ 설정 완료 확인

모든 Secrets 설정 후:

1. GitHub Actions 탭으로 이동
2. "CI/CD Pipeline" 워크플로우 확인
3. "Run workflow" 클릭하여 테스트 실행
4. 모든 단계가 성공적으로 완료되는지 확인

## 🚨 문제 해결

### Vercel 배포 실패

- `VERCEL_TOKEN`이 올바른지 확인
- `VERCEL_ORG_ID`와 `VERCEL_PROJECT_ID`가 정확한지 확인
- Vercel 프로젝트가 올바르게 연결되어 있는지 확인

### Lighthouse CI 실패

- `LHCI_GITHUB_APP_TOKEN`이 올바른지 확인
- GitHub App이 올바르게 설치되어 있는지 확인

### Slack 알림 실패

- `SLACK_WEBHOOK_URL`이 올바른지 확인
- Slack 워크스페이스에서 Webhook이 활성화되어 있는지 확인

## 📚 추가 리소스

- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Lighthouse CI Documentation](https://github.com/GoogleChrome/lighthouse-ci)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
