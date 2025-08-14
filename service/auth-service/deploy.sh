#!/bin/bash

# Auth Service Docker 배포 스크립트

set -e

echo "🚀 Auth Service Docker 배포 시작..."

# 1. Docker 이미지 빌드
echo "📦 Docker 이미지 빌드 중..."
docker build -t auth-service:latest .

# 2. 기존 컨테이너 정리
echo "🧹 기존 컨테이너 정리 중..."
docker stop auth-service 2>/dev/null || true
docker rm auth-service 2>/dev/null || true

# 3. 새 컨테이너 실행
echo "▶️ 새 컨테이너 실행 중..."
docker run -d \
  --name auth-service \
  --restart unless-stopped \
  -p 8008:8008 \
  --env-file .env \
  auth-service:latest

# 4. 헬스체크
echo "🏥 헬스체크 중..."
sleep 10
if curl -f http://localhost:8008/health > /dev/null 2>&1; then
    echo "✅ 배포 성공! 서비스가 정상적으로 실행 중입니다."
    echo "🌐 서비스 URL: http://localhost:8008"
    echo "📊 헬스체크: http://localhost:8008/health"
else
    echo "❌ 배포 실패! 서비스가 정상적으로 응답하지 않습니다."
    docker logs auth-service
    exit 1
fi

echo "🎉 배포 완료!"
