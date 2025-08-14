# Railway Docker 설정 스크립트 (PowerShell)

Write-Host "🚀 Railway Docker 설정 시작..." -ForegroundColor Green

# 1. Railway CLI 설치 확인
try {
    $railwayVersion = railway --version
    Write-Host "✅ Railway CLI가 이미 설치되어 있습니다: $railwayVersion" -ForegroundColor Green
} catch {
    Write-Host "📦 Railway CLI 설치 중..." -ForegroundColor Yellow
    npm install -g @railway/cli
}

# 2. Railway 로그인 확인
Write-Host "🔐 Railway 로그인 상태 확인..." -ForegroundColor Cyan
try {
    railway whoami | Out-Null
    Write-Host "✅ Railway에 로그인되어 있습니다." -ForegroundColor Green
} catch {
    Write-Host "⚠️ Railway에 로그인해야 합니다." -ForegroundColor Yellow
    railway login
}

# 3. 프로젝트 연결 확인
Write-Host "🔗 프로젝트 연결 상태 확인..." -ForegroundColor Cyan
try {
    railway status | Out-Null
    Write-Host "✅ Railway 프로젝트에 연결되어 있습니다." -ForegroundColor Green
} catch {
    Write-Host "⚠️ Railway 프로젝트에 연결해야 합니다." -ForegroundColor Yellow
    railway link
}

# 4. Docker 빌더 설정
Write-Host "🐳 Docker 빌더 설정 중..." -ForegroundColor Cyan
railway variables set RAILWAY_BUILDER="DOCKERFILE"

# 5. 환경 변수 설정 (필수)
Write-Host "🔧 필수 환경 변수 설정 중..." -ForegroundColor Cyan

# 데이터베이스 URL 설정
$DATABASE_URL = Read-Host "Railway PostgreSQL URL을 입력하세요"
railway variables set DATABASE_URL="$DATABASE_URL"

# JWT 시크릿 키 설정
$JWT_SECRET_KEY = Read-Host "JWT 시크릿 키를 입력하세요"
railway variables set JWT_SECRET_KEY="$JWT_SECRET_KEY"

# 기본 환경 변수 설정
railway variables set PORT="8008"
railway variables set ENVIRONMENT="production"
railway variables set DB_POOL_SIZE="20"
railway variables set DB_MAX_OVERFLOW="30"
railway variables set DB_POOL_TIMEOUT="30"
railway variables set DB_POOL_RECYCLE="3600"
railway variables set DB_POOL_PRE_PING="true"
railway variables set DB_ECHO="false"
railway variables set JWT_ALGORITHM="HS256"
railway variables set JWT_ACCESS_TOKEN_EXPIRE_MINUTES="30"
railway variables set LOG_LEVEL="INFO"

Write-Host "✅ 환경 변수 설정 완료!" -ForegroundColor Green

# 6. 설정 확인
Write-Host "📋 현재 설정 확인 중..." -ForegroundColor Cyan
railway variables list

# 7. 배포 준비 완료
Write-Host ""
Write-Host "🎉 Railway Docker 설정 완료!" -ForegroundColor Green
Write-Host ""
Write-Host "다음 단계:" -ForegroundColor Yellow
Write-Host "1. Railway 대시보드에서 Builder를 'Dockerfile'로 변경" -ForegroundColor White
Write-Host "2. GitHub에 코드 push: git add . && git commit -m 'Docker 배포 설정' && git push" -ForegroundColor White
Write-Host "3. Railway에서 자동 배포 확인" -ForegroundColor White
Write-Host ""
Write-Host "또는 수동 배포:" -ForegroundColor Yellow
Write-Host "railway up" -ForegroundColor White
