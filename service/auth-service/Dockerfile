# Python 3.11 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 환경 설정
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Python 의존성 파일 복사
COPY requirements.txt .

# Python 패키지 설치 (캐시 제거 및 강제 재설치)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip list && \
    python -c "import uvicorn; print('uvicorn 설치 확인:', uvicorn.__version__)"

# 애플리케이션 코드 복사
COPY . .

# 포트 노출 (Railway 동적 포트 지원)
EXPOSE 8008

# 헬스체크 추가
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8008/health || exit 1

# 애플리케이션 실행 (Railway 동적 포트 지원)
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8008"]
