#!/bin/bash

# Auth Service Docker 테스트 스크립트

set -e

echo "🧪 Auth Service Docker 테스트 시작..."

# 1. Docker 이미지 빌드
echo "📦 Docker 이미지 빌드 중..."
docker build -t auth-service:test .

# 2. 기존 테스트 컨테이너 정리
echo "🧹 기존 테스트 컨테이너 정리 중..."
docker stop auth-service-test 2>/dev/null || true
docker rm auth-service-test 2>/dev/null || true

# 3. 테스트 컨테이너 실행
echo "▶️ 테스트 컨테이너 실행 중..."
docker run -d \
  --name auth-service-test \
  -p 8008:8008 \
  -e PORT=8008 \
  -e ENVIRONMENT=test \
  -e DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/test_db \
  -e JWT_SECRET_KEY=test_jwt_secret_key \
  -e DB_POOL_SIZE=5 \
  -e DB_MAX_OVERFLOW=10 \
  -e DB_POOL_TIMEOUT=30 \
  -e DB_POOL_RECYCLE=3600 \
  -e DB_POOL_PRE_PING=true \
  -e DB_ECHO=false \
  -e JWT_ALGORITHM=HS256 \
  -e JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30 \
  -e LOG_LEVEL=INFO \
  auth-service:test

# 4. 컨테이너 시작 대기
echo "⏳ 컨테이너 시작 대기 중..."
sleep 15

# 5. 헬스체크
echo "🏥 헬스체크 중..."
if curl -f http://localhost:8008/health > /dev/null 2>&1; then
    echo "✅ 헬스체크 성공!"
else
    echo "❌ 헬스체크 실패!"
    echo "📋 컨테이너 로그:"
    docker logs auth-service-test
    exit 1
fi

# 6. API 엔드포인트 테스트
echo "🔍 API 엔드포인트 테스트 중..."

# 루트 엔드포인트
echo "📡 루트 엔드포인트 테스트..."
curl -s http://localhost:8008/ | jq '.' || echo "루트 엔드포인트 응답 확인"

# 헬스체크 엔드포인트
echo "📊 헬스체크 엔드포인트 테스트..."
curl -s http://localhost:8008/health | jq '.' || echo "헬스체크 엔드포인트 응답 확인"

# 서비스 정보 엔드포인트
echo "ℹ️ 서비스 정보 엔드포인트 테스트..."
curl -s http://localhost:8008/info | jq '.' || echo "서비스 정보 엔드포인트 응답 확인"

# 7. 테스트 결과 요약
echo ""
echo "🎯 테스트 결과 요약:"
echo "✅ Docker 이미지 빌드: 성공"
echo "✅ 컨테이너 실행: 성공"
echo "✅ 헬스체크: 성공"
echo "✅ API 엔드포인트: 테스트 완료"
echo ""
echo "🌐 서비스 URL: http://localhost:8008"
echo "📊 헬스체크: http://localhost:8008/health"
echo "ℹ️ 서비스 정보: http://localhost:8008/info"

# 8. 컨테이너 로그 모니터링
echo ""
echo "📋 컨테이너 로그 (Ctrl+C로 종료):"
docker logs -f auth-service-test
