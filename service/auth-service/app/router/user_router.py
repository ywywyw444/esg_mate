"""
Auth Service Router - Controller와 Service 계층 연결
"""
import logging
from fastapi import APIRouter, Cookie, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

# 로거 설정
logger = logging.getLogger(__name__)

# 의존성 및 스키마 import
from app.common.database.database import get_db
from app.domain.user_schema import LoginRequest, SignupRequest, AuthResponse
from app.domain.user_controller import user_controller

# Router 생성
auth_router = APIRouter(prefix="/auth-service", tags=["Auth"])

# ==================== 로그인 엔드포인트 ====================

@auth_router.post("/login", summary="로그인")
async def login_process(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """사용자 로그인 처리"""
    logger.info("🔐 로그인 POST 요청 받음")
    
    try:
        # 요청 데이터 파싱
        form_data = await request.json()
        logger.info(f"로그인 시도: {form_data.get('auth_id', 'N/A')}")
        
        # LoginRequest 스키마로 데이터 검증
        login_data = LoginRequest(
            auth_id=form_data.get('auth_id'),
            auth_pw=form_data.get('auth_pw')
        )
        
        # Controller를 통한 로그인 처리
        result = await user_controller.process_login(db, login_data)
        
        if result.success:
            logger.info(f"✅ 로그인 성공: {login_data.auth_id}")
        else:
            logger.warning(f"❌ 로그인 실패: {login_data.auth_id} - {result.message}")
        
        return result
        
    except Exception as e:
        logger.error(f"로그인 처리 중 오류: {str(e)}")
        return AuthResponse(
            success=False,
            message=f"로그인 처리 중 오류가 발생했습니다: {str(e)}"
        )

# ==================== 회원가입 엔드포인트 ====================

@auth_router.post("/signup", summary="회원가입")
async def signup_process(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """사용자 회원가입 처리"""
    logger.info("📝 회원가입 POST 요청 받음")
    
    try:
        # 요청 데이터 파싱
        form_data = await request.json()
        
        # SignupRequest 스키마로 데이터 검증
        signup_data = SignupRequest(
            company_id=form_data.get('company_id'),
            industry=form_data.get('industry'),
            email=form_data.get('email'),
            name=form_data.get('name'),
            age=form_data.get('age'),
            auth_id=form_data.get('auth_id'),
            auth_pw=form_data.get('auth_pw')
        )
        
        logger.info("=== 회원가입 요청 데이터 ===")
        logger.info(f"회사 ID: {signup_data.company_id}")
        logger.info(f"산업: {signup_data.industry}")
        logger.info(f"이메일: {signup_data.email}")
        logger.info(f"이름: {signup_data.name}")
        logger.info(f"나이: {signup_data.age}")
        logger.info(f"인증 ID: {signup_data.auth_id}")
        logger.info(f"인증 비밀번호: [PROTECTED]")
        logger.info("==========================")
        
        # Controller를 통한 회원가입 처리
        result = await user_controller.process_signup(db, signup_data)
        
        if result.success:
            logger.info(f"✅ 회원가입 성공: {signup_data.email}")
        else:
            logger.warning(f"❌ 회원가입 실패: {signup_data.email} - {result.message}")
        
        return result
        
    except Exception as e:
        logger.error(f"회원가입 처리 중 오류: {str(e)}")
        return AuthResponse(
            success=False,
            message=f"회원가입 처리 중 오류가 발생했습니다: {str(e)}"
        )

# ==================== 로그아웃 엔드포인트 ====================

@auth_router.post("/logout", summary="로그아웃")
async def logout_process(session_token: str | None = Cookie(None)):
    """사용자 로그아웃 처리"""
    logger.info("🚪 로그아웃 POST 요청 받음")
    
    try:
        print(f"로그아웃 요청 - 받은 세션 토큰: {session_token}")
        
        # Controller를 통한 로그아웃 처리
        result = await user_controller.process_logout(session_token or "")
        
        if result.success:
            # 로그아웃 응답 생성
            response = JSONResponse(result.dict())
            
            # 인증 쿠키 삭제
            response.delete_cookie(
                key="session_token",
                path="/",
            )
            
            logger.info("✅ 로그아웃 완료 - 인증 쿠키 삭제됨")
            return response
        else:
            return JSONResponse(result.dict())
            
    except Exception as e:
        logger.error(f"로그아웃 처리 중 오류: {str(e)}")
        return JSONResponse({
            "success": False,
            "message": f"로그아웃 처리 중 오류가 발생했습니다: {str(e)}"
        })

# ==================== 프로필 조회 엔드포인트 ====================

@auth_router.get("/profile", summary="사용자 프로필 조회")
async def get_profile(
    session_token: str | None = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    """세션 토큰으로 사용자 프로필 조회"""
    logger.info("👤 프로필 조회 GET 요청 받음")
    
    try:
        print(f"프로필 요청 - 받은 세션 토큰: {session_token}")
        
        if not session_token:
            raise HTTPException(status_code=401, detail="인증 쿠키가 없습니다.")
        
        # Controller를 통한 프로필 조회 처리
        result = await user_controller.process_profile_get(db, session_token)
        
        if result.success:
            logger.info(f"✅ 프로필 조회 성공: {session_token}")
        else:
            logger.warning(f"❌ 프로필 조회 실패: {session_token} - {result.message}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"프로필 조회 오류: {e}")
        raise HTTPException(status_code=401, detail=str(e))

# ==================== 세션 관리 엔드포인트 ====================

@auth_router.get("/session/status", summary="세션 상태 조회")
async def get_session_status():
    """활성 세션 상태 조회"""
    logger.info("📊 세션 상태 조회 GET 요청 받음")
    
    try:
        result = await user_controller.get_session_status()
        logger.info(f"✅ 세션 상태 조회 성공: {result.get('active_sessions', 0)}개 활성 세션")
        return result
        
    except Exception as e:
        logger.error(f"세션 상태 조회 중 오류: {str(e)}")
        return {
            "active_sessions": 0,
            "status": "error",
            "error": str(e)
        }

@auth_router.post("/session/cleanup", summary="만료된 세션 정리")
async def cleanup_expired_sessions():
    """만료된 세션 정리"""
    logger.info("🧹 만료된 세션 정리 POST 요청 받음")
    
    try:
        result = await user_controller.cleanup_sessions()
        logger.info(f"✅ 세션 정리 완료: {result.get('cleaned_sessions', 0)}개 세션 정리됨")
        return result
        
    except Exception as e:
        logger.error(f"세션 정리 중 오류: {str(e)}")
        return {
            "cleaned_sessions": 0,
            "status": "error",
            "error": str(e)
        }

# ==================== 헬스체크 엔드포인트 ====================

@auth_router.get("/health", summary="서비스 상태 확인")
async def health_check():
    """인증 서비스 상태 확인"""
    return {
        "status": "healthy",
        "service": "auth-service",
        "endpoints": {
            "login": "/auth-service/login",
            "signup": "/auth-service/signup",
            "logout": "/auth-service/logout",
            "profile": "/auth-service/profile",
            "session_status": "/auth-service/session/status",
            "session_cleanup": "/auth-service/session/cleanup"
        }
    }