#!/bin/bash

# Railway Docker 설정 스크립트

set -e

echo "🚀 Railway Docker 설정 시작..."

# 1. Railway CLI 설치 확인
if ! command -v railway &> /dev/null; then
    echo "📦 Railway CLI 설치 중..."
    npm install -g @railway/cli
else
    echo "✅ Railway CLI가 이미 설치되어 있습니다."
fi

# 2. Railway 로그인 확인
echo "🔐 Railway 로그인 상태 확인..."
if ! railway whoami &> /dev/null; then
    echo "⚠️ Railway에 로그인해야 합니다."
    railway login
else
    echo "✅ Railway에 로그인되어 있습니다."
fi

# 3. 프로젝트 연결 확인
echo "🔗 프로젝트 연결 상태 확인..."
if ! railway status &> /dev/null; then
    echo "⚠️ Railway 프로젝트에 연결해야 합니다."
    railway link
else
    echo "✅ Railway 프로젝트에 연결되어 있습니다."
fi

# 4. Docker 빌더 설정
echo "🐳 Docker 빌더 설정 중..."
railway variables set RAILWAY_BUILDER="DOCKERFILE"

# 5. 환경 변수 설정 (필수)
echo "🔧 필수 환경 변수 설정 중..."

# 데이터베이스 URL 설정
read -p "Railway PostgreSQL URL을 입력하세요: " DATABASE_URL
railway variables set DATABASE_URL="$DATABASE_URL"

# JWT 시크릿 키 설정
read -p "JWT 시크릿 키를 입력하세요: " JWT_SECRET_KEY
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

echo "✅ 환경 변수 설정 완료!"

# 6. 설정 확인
echo "📋 현재 설정 확인 중..."
railway variables list

# 7. 배포 준비 완료
echo ""
echo "🎉 Railway Docker 설정 완료!"
echo ""
echo "다음 단계:"
echo "1. Railway 대시보드에서 Builder를 'Dockerfile'로 변경"
echo "2. GitHub에 코드 push: git add . && git commit -m 'Docker 배포 설정' && git push"
echo "3. Railway에서 자동 배포 확인"
echo ""
echo "또는 수동 배포:"
echo "railway up"
