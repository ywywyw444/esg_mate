"""
Auth 서비스 메인 애플리케이션 진입점 - 개선된 구조
"""
import os
import logging
import sys
import traceback
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Request, Depends, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import APIRouter

# Router import
from app.router.user_router import auth_router
from app.domain.user_controller import user_controller

# 데이터베이스 import
from app.common.database.database import initialize_database, shutdown_database, get_pool_status

# 환경 변수 로드
if os.getenv("RAILWAY_ENVIRONMENT") != "true":
    load_dotenv()

# Railway 환경변수 처리
PORT = os.getenv("PORT", "8008")
if not PORT.isdigit():
    PORT = "8008"

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("auth_service")

# ==================== 애플리케이션 라이프사이클 관리 ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 라이프사이클 관리"""
    # 시작 시
    logger.info("🚀 Auth Service 시작 중...")
    
    try:
        # 데이터베이스 초기화
        await initialize_database()
        logger.info("✅ 데이터베이스 초기화 완료")
        
        # 기타 초기화 작업
        logger.info("✅ Auth Service 초기화 완료")
        
    except Exception as e:
        logger.error(f"❌ Auth Service 초기화 실패: {str(e)}")
        raise
    
    yield
    
    # 종료 시
    logger.info("🛑 Auth Service 종료 중...")
    
    try:
        # 데이터베이스 정리
        await shutdown_database()
        logger.info("✅ 데이터베이스 정리 완료")
        
        # 기타 정리 작업
        logger.info("✅ Auth Service 정리 완료")
        
    except Exception as e:
        logger.error(f"❌ Auth Service 정리 중 오류: {str(e)}")

# ==================== FastAPI 애플리케이션 생성 ====================

app = FastAPI(
    title="Auth Service API",
    description="사용자 인증 및 세션 관리 서비스",
    version="1.0.0",
    lifespan=lifespan
)

# ==================== 미들웨어 설정 ====================

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# 신뢰할 수 있는 호스트 설정
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # 프로덕션에서는 특정 호스트로 제한
)

# ==================== 라우터 등록 ====================

app.include_router(auth_router)

# ==================== 기본 엔드포인트 ====================

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "Auth Service API",
        "version": "1.0.0",
        "status": "running",
        "description": "사용자 인증 및 세션 관리 서비스"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    try:
        # 데이터베이스 연결 상태 확인
        pool_status = await get_pool_status()
        
        return {
            "status": "healthy",
            "service": "auth-service",
            "timestamp": "2025-01-13T08:00:00Z",
            "database": {
                "status": "connected",
                "pool": pool_status
            },
            "endpoints": {
                "auth": "/auth-service",
                "user": "/user",
                "health": "/health"
            }
        }
    except Exception as e:
        logger.error(f"❌ 헬스 체크 실패: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "auth-service",
            "error": str(e),
            "timestamp": "2025-01-13T08:00:00Z"
        }

@app.get("/info")
async def service_info():
    """서비스 정보 엔드포인트"""
    return {
        "service": "auth-service",
        "version": "1.0.0",
        "description": "사용자 인증 및 세션 관리 마이크로서비스",
        "features": [
            "사용자 로그인/로그아웃",
            "사용자 회원가입",
            "JWT 토큰 기반 인증",
            "세션 관리",
            "Railway PostgreSQL 연동"
        ],
        "architecture": {
            "pattern": "Clean Architecture",
            "layers": ["Router", "Controller", "Service", "Repository", "Entity"],
            "database": "PostgreSQL (Railway)",
            "async": True
        }
    }

# ==================== 요청/응답 로깅 미들웨어 ====================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """요청/응답 로깅 미들웨어"""
    client_host = request.headers.get("x-forwarded-for") or (request.client.host if request.client else "unknown")
    
    # 요청 로깅
    logger.info(f"📥 요청: {request.method} {request.url.path} (클라이언트: {client_host})")
    
    try:
        # 요청 처리
        response = await call_next(request)
        
        # 응답 로깅
        logger.info(f"📤 응답: {response.status_code} - {request.method} {request.url.path}")
        
        return response
        
    except Exception as e:
        # 오류 로깅
        logger.error(f"❌ 요청 처리 중 오류: {str(e)}")
        logger.error(traceback.format_exc())
        raise

# ==================== 예외 처리 핸들러 ====================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """전역 예외 처리 핸들러"""
    logger.error(f"❌ 전역 예외 발생: {str(exc)}")
    logger.error(f"📍 요청: {request.method} {request.url.path}")
    logger.error(traceback.format_exc())
    
    return {
        "success": False,
        "message": "서버 내부 오류가 발생했습니다.",
        "error": str(exc),
        "path": str(request.url.path)
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP 예외 처리 핸들러"""
    logger.warning(f"⚠️ HTTP 예외 발생: {exc.status_code} - {exc.detail}")
    logger.warning(f"📍 요청: {request.method} {request.url.path}")
    
    return {
        "success": False,
        "message": exc.detail,
        "status_code": exc.status_code,
        "path": str(request.url.path)
    }

# ==================== 메인 실행 ====================

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"🚀 Auth Service 시작 - 포트: {PORT}")
    
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=int(PORT), 
        reload=True,
        log_level="info"
    )
