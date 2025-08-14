"""
User Controller - CrossEntity 패턴으로 비즈니스 로직 및 데이터 검증 담당
"""
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.database.database import get_db
from app.domain.user_schema import (
    LoginRequest, SignupRequest, AuthResponse, 
    UserEntity, UserCreateEntity, UserUpdateEntity
)
from app.domain.service.auth_service import AuthService
from app.domain.user.user_repository import UserRepository

logger = logging.getLogger("auth_service_controller")

router = APIRouter(prefix="/user", tags=["User"])

class UserController:
    """사용자 컨트롤러 - CrossEntity 패턴"""
    
    def __init__(self):
        self.auth_service = AuthService()
        self.user_repository = UserRepository()
    
    # ==================== 데이터 검증 메서드 ====================
    
    async def validate_login_data(self, login_data: LoginRequest) -> Dict[str, Any]:
        """로그인 데이터 검증"""
        try:
            # 기본 유효성 검사
            if not login_data.auth_id or not login_data.auth_pw:
                raise ValueError("인증 ID와 비밀번호는 필수입니다.")
            
            # 길이 검사
            if len(login_data.auth_id) < 1:
                raise ValueError("인증 ID는 최소 1자 이상이어야 합니다.")
            
            if len(login_data.auth_pw) < 1:
                raise ValueError("비밀번호는 최소 1자 이상이어야 합니다.")
            
            logger.info(f"✅ 로그인 데이터 검증 완료: {login_data.auth_id}")
            return {"valid": True, "data": login_data}
            
        except Exception as e:
            logger.error(f"❌ 로그인 데이터 검증 실패: {str(e)}")
            return {"valid": False, "error": str(e)}
    
    async def validate_signup_data(self, signup_data: SignupRequest) -> Dict[str, Any]:
        """회원가입 데이터 검증"""
        try:
            # 필수 필드 검사
            required_fields = ['company_id', 'industry', 'email', 'name', 'age', 'auth_id', 'auth_pw']
            for field in required_fields:
                if not getattr(signup_data, field):
                    raise ValueError(f"{field}는 필수 필드입니다.")
            
            # 이메일 형식 검사
            if '@' not in signup_data.email or '.' not in signup_data.email:
                raise ValueError("올바른 이메일 형식이 아닙니다.")
            
            # 비밀번호 길이 검사
            if len(signup_data.auth_pw) < 6:
                raise ValueError("비밀번호는 최소 6자 이상이어야 합니다.")
            
            # 나이 형식 검사 (숫자 또는 숫자+문자)
            if not signup_data.age.replace('세', '').replace('살', '').isdigit():
                raise ValueError("나이는 숫자 형식이어야 합니다.")
            
            logger.info(f"✅ 회원가입 데이터 검증 완료: {signup_data.email}")
            return {"valid": True, "data": signup_data}
            
        except Exception as e:
            logger.error(f"❌ 회원가입 데이터 검증 실패: {str(e)}")
            return {"valid": False, "error": str(e)}
    
    # ==================== 비즈니스 로직 메서드 ====================
    
    async def process_login(self, db: AsyncSession, login_data: LoginRequest) -> AuthResponse:
        """로그인 처리 비즈니스 로직"""
        try:
            # 1단계: 데이터 검증
            validation_result = await self.validate_login_data(login_data)
            if not validation_result["valid"]:
                return AuthResponse(
                    success=False,
                    message=f"데이터 검증 실패: {validation_result['error']}"
                )
            
            # 2단계: 인증 서비스 호출
            auth_result = await self.auth_service.authenticate_user(db, login_data)
            
            # 3단계: 결과 로깅 및 반환
            if auth_result.success:
                logger.info(f"🎉 로그인 성공: {login_data.auth_id}")
            else:
                logger.warning(f"⚠️ 로그인 실패: {login_data.auth_id} - {auth_result.message}")
            
            return auth_result
            
        except Exception as e:
            logger.error(f"❌ 로그인 처리 중 오류: {str(e)}")
            return AuthResponse(
                success=False,
                message=f"로그인 처리 중 오류가 발생했습니다: {str(e)}"
            )
    
    async def process_signup(self, db: AsyncSession, signup_data: SignupRequest) -> AuthResponse:
        """회원가입 처리 비즈니스 로직"""
        try:
            # 1단계: 데이터 검증
            validation_result = await self.validate_signup_data(signup_data)
            if not validation_result["valid"]:
                return AuthResponse(
                    success=False,
                    message=f"데이터 검증 실패: {validation_result['error']}"
                )
            
            # 2단계: 인증 서비스 호출
            auth_result = await self.auth_service.register_user(db, signup_data)
            
            # 3단계: 결과 로깅 및 반환
            if auth_result.success:
                logger.info(f"🎉 회원가입 성공: {signup_data.email}")
            else:
                logger.warning(f"⚠️ 회원가입 실패: {signup_data.email} - {auth_result.message}")
            
            return auth_result
            
        except Exception as e:
            logger.error(f"❌ 회원가입 처리 중 오류: {str(e)}")
            return AuthResponse(
                success=False,
                message=f"회원가입 처리 중 오류가 발생했습니다: {str(e)}"
            )
    
    async def process_logout(self, session_token: str) -> AuthResponse:
        """로그아웃 처리 비즈니스 로직"""
        try:
            # 1단계: 세션 토큰 검증
            if not session_token:
                return AuthResponse(
                    success=False,
                    message="세션 토큰이 제공되지 않았습니다."
                )
            
            # 2단계: 인증 서비스 호출
            auth_result = await self.auth_service.logout_user(session_token)
            
            # 3단계: 결과 로깅 및 반환
            if auth_result.success:
                logger.info(f"🎉 로그아웃 성공: {session_token}")
            else:
                logger.warning(f"⚠️ 로그아웃 실패: {session_token} - {auth_result.message}")
            
            return auth_result
            
        except Exception as e:
            logger.error(f"❌ 로그아웃 처리 중 오류: {str(e)}")
            return AuthResponse(
                success=False,
                message=f"로그아웃 처리 중 오류가 발생했습니다: {str(e)}"
            )
    
    async def process_profile_get(self, db: AsyncSession, session_token: str) -> AuthResponse:
        """프로필 조회 처리 비즈니스 로직"""
        try:
            # 1단계: 세션 토큰 검증
            if not session_token:
                return AuthResponse(
                    success=False,
                    message="세션 토큰이 제공되지 않았습니다."
                )
            
            # 2단계: 인증 서비스 호출
            auth_result = await self.auth_service.get_user_profile(db, session_token)
            
            # 3단계: 결과 로깅 및 반환
            if auth_result.success:
                logger.info(f"🎉 프로필 조회 성공: {session_token}")
            else:
                logger.warning(f"⚠️ 프로필 조회 실패: {session_token} - {auth_result.message}")
            
            return auth_result
            
        except Exception as e:
            logger.error(f"❌ 프로필 조회 처리 중 오류: {str(e)}")
            return AuthResponse(
                success=False,
                message=f"프로필 조회 처리 중 오류가 발생했습니다: {str(e)}"
            )
    
    # ==================== 세션 관리 메서드 ====================
    
    async def get_session_status(self) -> Dict[str, Any]:
        """세션 상태 조회"""
        try:
            active_count = await self.auth_service.get_active_sessions_count()
            return {
                "active_sessions": active_count,
                "status": "healthy"
            }
        except Exception as e:
            logger.error(f"❌ 세션 상태 조회 중 오류: {str(e)}")
            return {
                "active_sessions": 0,
                "status": "error",
                "error": str(e)
            }
    
    async def cleanup_sessions(self) -> Dict[str, Any]:
        """만료된 세션 정리"""
        try:
            cleaned_count = await self.auth_service.cleanup_expired_sessions()
            return {
                "cleaned_sessions": cleaned_count,
                "status": "success"
            }
        except Exception as e:
            logger.error(f"❌ 세션 정리 중 오류: {str(e)}")
            return {
                "cleaned_sessions": 0,
                "status": "error",
                "error": str(e)
            }

# 컨트롤러 인스턴스 생성
user_controller = UserController()

# ==================== API 엔드포인트 ====================

@router.get("/")
async def get_user():
    """사용자 기본 엔드포인트"""
    return {"message": "User Controller Endpoint"}

@router.get("/session/status")
async def get_session_status():
    """세션 상태 조회"""
    return await user_controller.get_session_status()

@router.post("/session/cleanup")
async def cleanup_sessions():
    """만료된 세션 정리"""
    return await user_controller.cleanup_sessions()
