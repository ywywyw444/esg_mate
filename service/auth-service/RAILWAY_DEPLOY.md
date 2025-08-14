# Railway Docker 배포 가이드

## 🚀 Railway에서 Docker 기반 배포하기

### 1. Railway 프로젝트 설정

#### A. Railway CLI 설치
```bash
npm install -g @railway/cli
```

#### B. Railway 로그인 및 프로젝트 연결
```bash
railway login
railway link
```

### 2. 환경 변수 설정

#### A. Railway 대시보드에서 설정
```bash
# Railway 대시보드 → Variables 탭에서 설정
DATABASE_URL=postgresql+asyncpg://postgres:password@your-railway-postgres-url
JWT_SECRET_KEY=your_super_secret_jwt_key_here
PORT=8008
ENVIRONMENT=production
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=30
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
DB_POOL_PRE_PING=true
DB_ECHO=false
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
LOG_LEVEL=INFO
```

#### B. Railway CLI로 설정
```bash
railway variables set DATABASE_URL="your_railway_postgres_url"
railway variables set JWT_SECRET_KEY="your_secret_key"
railway variables set PORT="8008"
railway variables set ENVIRONMENT="production"
```

### 3. Docker 배포 방법

#### A. 자동 배포 (GitHub 연동)
```bash
# 1. GitHub 저장소에 코드 push
git add .
git commit -m "Docker 배포 준비 완료"
git push origin main

# 2. Railway에서 자동으로 Docker 이미지 빌드 및 배포
```

#### B. 수동 배포
```bash
# 1. Docker 이미지 빌드
docker build -t auth-service:latest .

# 2. Railway에 배포
railway up
```

### 4. 배포 확인

#### A. 배포 상태 확인
```bash
railway status
```

#### B. 로그 확인
```bash
railway logs
```

#### C. 서비스 URL 확인
```bash
railway domain
```

### 5. 문제 해결

#### A. 배포 실패 시
```bash
# 1. 로그 확인
railway logs

# 2. 환경 변수 확인
railway variables list

# 3. 재배포
railway up
```

#### B. 헬스체크 실패 시
```bash
# 1. 서비스 상태 확인
railway status

# 2. 수동 헬스체크
curl https://your-railway-domain.railway.app/health
```

### 6. 로컬 Docker 테스트

#### A. docker-compose로 테스트
```bash
# 1. 환경 변수 파일 생성
cp env.example .env
# .env 파일 편집

# 2. Docker Compose 실행
docker-compose up -d

# 3. 테스트
curl http://localhost:8008/health
```

#### B. 단일 컨테이너로 테스트
```bash
# 1. 이미지 빌드
docker build -t auth-service:test .

# 2. 컨테이너 실행
docker run -d \
  --name auth-service-test \
  -p 8008:8008 \
  --env-file .env \
  auth-service:test

# 3. 테스트
curl http://localhost:8008/health
```

### 7. 모니터링

#### A. Railway 대시보드
- Deployments: 배포 상태 및 히스토리
- Variables: 환경 변수 관리
- Metrics: 서비스 성능 모니터링
- Logs: 실시간 로그 확인

#### B. 헬스체크 엔드포인트
```bash
# 기본 헬스체크
GET /health

# 상세 서비스 정보
GET /info

# 세션 상태
GET /auth-service/session/status
```

### 8. 성능 최적화

#### A. Docker 이미지 최적화
- 멀티 스테이지 빌드 사용
- 불필요한 파일 제외 (.dockerignore)
- 레이어 캐싱 최적화

#### B. Railway 설정 최적화
- 적절한 인스턴스 크기 선택
- 자동 스케일링 설정
- 연결 풀 크기 조정

## 🎯 성공적인 배포를 위한 체크리스트

- [ ] Dockerfile이 올바르게 작성됨
- [ ] .dockerignore 파일이 최적화됨
- [ ] 환경 변수가 Railway에 설정됨
- [ ] requirements.txt에 모든 의존성이 포함됨
- [ ] 로컬에서 Docker 테스트 완료
- [ ] GitHub Actions가 정상 작동함
- [ ] Railway 프로젝트가 연결됨

## 🚨 주의사항

1. **환경 변수**: 프로덕션에서는 민감한 정보를 환경 변수로 관리
2. **포트**: Railway는 동적 포트를 사용하므로 `$PORT` 환경 변수 활용
3. **데이터베이스**: Railway PostgreSQL 연결 문자열 확인
4. **로깅**: 프로덕션 환경에서는 적절한 로그 레벨 설정

---

**Railway Docker 배포 완료!** 🎉
