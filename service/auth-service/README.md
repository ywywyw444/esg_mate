# Auth Service

사용자 인증 및 세션 관리를 위한 마이크로서비스입니다. Clean Architecture 패턴을 적용하여 설계되었으며, Railway PostgreSQL과 연동됩니다.

## 🏗️ 아키텍처

### 계층 구조
```
┌─────────────────┐
│     Router      │ ← HTTP 요청/응답 처리
├─────────────────┤
│   Controller    │ ← CrossEntity 패턴, 비즈니스 로직
├─────────────────┤
│     Service     │ ← async def로 기능 정의
├─────────────────┤
│   Repository    │ ← 인증 데이터 관리, 세션 관리
├─────────────────┤
│     Entity      │ ← Base 클래스, DB 연결
└─────────────────┘
```

### 주요 컴포넌트

- **Schema**: Pydantic BaseModel + SQLAlchemy 모델 통합 정의
- **Controller**: CrossEntity 패턴으로 비즈니스 로직 처리
- **Service**: async def로 인증 기능 구현
- **Repository**: 세션 관리 및 인증 데이터 관리
- **Entity**: SQLAlchemy Base 클래스로 DB 연결

## 🚀 기능

### 인증 기능
- ✅ 사용자 로그인/로그아웃
- ✅ 사용자 회원가입
- ✅ JWT 토큰 기반 인증
- ✅ 세션 관리 및 유효성 검증

### 보안 기능
- ✅ 비밀번호 해시화 (SHA256)
- ✅ 세션 타임아웃 관리
- ✅ 중복 로그인 방지
- ✅ 토큰 만료 처리

### 데이터베이스
- ✅ Railway PostgreSQL 연동
- ✅ 연결 풀 최적화
- ✅ 비동기 쿼리 처리
- ✅ 자동 테이블 생성

## 📁 프로젝트 구조

```
auth-service/
├── app/
│   ├── common/
│   │   ├── database/
│   │   │   └── database.py      # DB 연결 및 연결 풀 관리
│   │   └── utility/
│   │       └── jwt_utils.py     # JWT 토큰 관리
│   ├── domain/
│   │   ├── service/
│   │   │   └── auth_service.py  # 인증 서비스 (async)
│   │   ├── user_controller.py   # CrossEntity 컨트롤러
│   │   ├── user_schema.py       # Pydantic BaseModel + SQLAlchemy 모델
│   │   ├── user_repository.py   # 리포지토리 (세션 관리)
│   │   └── user_service.py      # 사용자 서비스
│   ├── router/
│   │   └── user_router.py       # API 라우터
│   └── main.py                  # 메인 애플리케이션
├── Dockerfile                   # Docker 컨테이너 설정
├── docker-compose.yml           # 로컬 개발용 Docker Compose
├── .dockerignore                # Docker 빌드 최적화
├── nixpacks.toml                # Railway 배포 설정
├── deploy.sh                    # Docker 배포 스크립트
├── test-docker.sh               # Docker 테스트 스크립트
├── requirements.txt             # 의존성 관리
├── env.example                  # 환경 변수 예시
├── RAILWAY_DEPLOY.md            # Railway 배포 상세 가이드
└── README.md                    # 프로젝트 문서
```

## 🛠️ 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
cp env.example .env
# .env 파일을 편집하여 실제 값으로 설정
```

### 3. 애플리케이션 실행
```bash
# 개발 모드
python -m app.main

# 또는 uvicorn 직접 실행
uvicorn app.main:app --host 0.0.0.0 --port 8008 --reload
```

### 4. Docker 실행

#### A. 단일 컨테이너 실행
```bash
docker build -t auth-service .
docker run -p 8008:8008 --env-file .env auth-service
```

#### B. Docker Compose로 실행 (PostgreSQL 포함)
```bash
# 환경 변수 파일 생성
cp env.example .env
# .env 파일 편집

# Docker Compose 실행
docker-compose up -d

# 테스트
curl http://localhost:8008/health
```

#### C. 배포 스크립트 사용
```bash
# Linux/Mac
./deploy.sh

# Windows PowerShell
.\deploy.sh
```

#### D. 테스트 스크립트 사용
```bash
# Linux/Mac
./test-docker.sh

# Windows PowerShell
.\test-docker.sh
```

## 🌐 API 엔드포인트

### 인증 관련
- `POST /auth-service/login` - 사용자 로그인
- `POST /auth-service/signup` - 사용자 회원가입
- `POST /auth-service/logout` - 사용자 로그아웃
- `GET /auth-service/profile` - 사용자 프로필 조회

### 세션 관리
- `GET /auth-service/session/status` - 세션 상태 조회
- `POST /auth-service/session/cleanup` - 만료된 세션 정리

### 시스템
- `GET /` - 서비스 정보
- `GET /health` - 헬스 체크
- `GET /info` - 상세 서비스 정보

## 🔧 환경 변수

### 필수 설정
- `DATABASE_URL`: Railway PostgreSQL 연결 문자열
- `JWT_SECRET_KEY`: JWT 토큰 암호화 키

### 데이터베이스 설정
- `DB_POOL_SIZE`: 연결 풀 크기 (기본값: 20)
- `DB_MAX_OVERFLOW`: 최대 오버플로우 (기본값: 30)
- `DB_POOL_TIMEOUT`: 연결 타임아웃 (기본값: 30초)

### 보안 설정
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: 토큰 만료 시간 (기본값: 30분)
- `SESSION_TIMEOUT_MINUTES`: 세션 타임아웃 (기본값: 30분)

## 🗄️ 데이터베이스 스키마

### User 테이블
```sql
CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    company_id TEXT NOT NULL,
    industry TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    age TEXT NOT NULL,
    auth_id TEXT NOT NULL UNIQUE,
    auth_pw TEXT NOT NULL
);
```

## 🔐 보안 기능

### 비밀번호 보안
- SHA256 해시화
- 솔트 적용
- 최소 길이 검증

### 세션 보안
- JWT 토큰 기반 인증
- 자동 만료 처리
- 중복 로그인 방지

### 데이터 검증
- Pydantic 스키마 검증
- 입력 데이터 정제
- SQL 인젝션 방지

## 📊 모니터링

### 연결 풀 모니터링
- 활성 연결 수 추적
- 연결 풀 상태 모니터링
- 자동 연결 정리

### 로깅
- 구조화된 로깅
- 요청/응답 추적
- 오류 상세 정보

## 🚀 Railway 배포

### Docker 기반 배포

#### 1. Railway CLI 설치
```bash
npm install -g @railway/cli
```

#### 2. 프로젝트 연결
```bash
railway login
railway link
```

#### 3. 환경 변수 설정
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

#### 4. Docker 배포
```bash
# 자동 배포 (GitHub 연동)
git add .
git commit -m "Docker 배포 준비 완료"
git push origin main

# 수동 배포
railway up
```

#### 5. 배포 확인
```bash
# 배포 상태 확인
railway status

# 로그 확인
railway logs

# 서비스 URL 확인
railway domain
```

### 상세 배포 가이드
자세한 배포 방법은 [RAILWAY_DEPLOY.md](./RAILWAY_DEPLOY.md) 파일을 참조하세요.

## 🧪 테스트

### 단위 테스트
```bash
pytest tests/ -v
```

### 통합 테스트
```bash
pytest tests/integration/ -v
```

### 커버리지 테스트
```bash
pytest --cov=app tests/ -v
```

## 🔄 개발 워크플로우

### 1. 기능 개발
- Feature 브랜치 생성
- Controller에 비즈니스 로직 추가
- Service에 async 함수 구현
- Repository에 데이터 접근 로직 추가

### 2. 테스트
- 단위 테스트 작성
- 통합 테스트 작성
- 커버리지 확인

### 3. 코드 품질
- Black으로 코드 포맷팅
- isort로 import 정렬
- flake8으로 린팅

## 📝 로그 형식

### 요청 로그
```
📥 요청: POST /auth-service/login (클라이언트: 192.168.1.1)
```

### 응답 로그
```
📤 응답: 200 - POST /auth-service/login
```

### 오류 로그
```
❌ 로그인 처리 중 오류: Database connection failed
```

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해 주세요.

---

**Auth Service v1.0.0** - Clean Architecture 기반의 안전하고 확장 가능한 인증 서비스
