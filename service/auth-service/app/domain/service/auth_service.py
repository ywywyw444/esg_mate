"""
Auth Service - 인증 관련 모든 기능을 async def로 정의
"""
import hashlib
import logging
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.user_schema import LoginRequest, SignupRequest, AuthResponse, UserEntity, UserModel
from app.common.utility.jwt_utils import JWTManager
from app.domain.user_repository import UserRepository

logger = logging.getLogger("auth_service")

class AuthService:
    """인증 서비스 - 모든 인증 관련 기능"""
    
    def __init__(self):
        self.user_repository = UserRepository()
        self.jwt_manager = JWTManager()
    
    # ==================== 로그인 기능 ====================
    
    async def authenticate_user(self, db: AsyncSession, login_data: LoginRequest) -> AuthResponse:
        """사용자 인증 및 로그인 처리"""
        try:
            logger.info(f"🔐 로그인 시도: {login_data.auth_id}")
            
            # 사용자 조회
            user = await self.user_repository.find_by_auth_id(db, login_data.auth_id)
            if not user:
                logger.warning(f"❌ 존재하지 않는 인증 ID: {login_data.auth_id}")
                return AuthResponse(
                    success=False,
                    message="존재하지 않는 인증 ID입니다."
                )
            
            # 비밀번호 검증
            if not await self._verify_password(login_data.auth_pw, user.auth_pw):
                logger.warning(f"❌ 비밀번호 불일치: {login_data.auth_id}")
                return AuthResponse(
                    success=False,
                    message="비밀번호가 일치하지 않습니다."
                )
            
            # JWT 토큰 생성
            token_data = {
                "user_id": user.id,
                "email": user.email,
                "auth_id": user.auth_id,
                "company_id": user.company_id
            }
            access_token = self.jwt_manager.create_access_token(token_data)
            
            # 세션 생성
            session_id = await self.user_repository.create_session(
                user.id, user.email, user.auth_id, user.company_id
            )
            
            logger.info(f"✅ 로그인 성공: {user.email} (ID: {user.id})")
            
            return AuthResponse(
                success=True,
                message="로그인이 완료되었습니다.",
                user_id=user.id,
                email=user.email,
                name=user.name,
                company_id=user.company_id,
                token=access_token
            )
            
        except Exception as e:
            logger.error(f"❌ 로그인 처리 중 오류: {str(e)}")
            return AuthResponse(
                success=False,
                message=f"로그인 처리 중 오류가 발생했습니다: {str(e)}"
            )
    
    # ==================== 회원가입 기능 ====================
    
    async def register_user(self, db: AsyncSession, signup_data: SignupRequest) -> AuthResponse:
        """새 사용자 회원가입"""
        try:
            logger.info(f"📝 회원가입 시도: {signup_data.email}")
            
            # 이메일 중복 확인
            existing_user = await self.user_repository.find_by_email(db, signup_data.email)
            if existing_user:
                logger.warning(f"❌ 이미 존재하는 이메일: {signup_data.email}")
                return AuthResponse(
                    success=False,
                    message="이미 존재하는 이메일입니다."
                )
            
            # 인증 ID 중복 확인
            existing_auth_user = await self.user_repository.find_by_auth_id(db, signup_data.auth_id)
            if existing_auth_user:
                logger.warning(f"❌ 이미 존재하는 인증 ID: {signup_data.auth_id}")
                return AuthResponse(
                    success=False,
                    message="이미 존재하는 인증 ID입니다."
                )
            
            # 비밀번호 해시화
            hashed_password = await self._hash_password(signup_data.auth_pw)
            
            # 사용자 생성 데이터 준비
            user_create_data = signup_data.copy()
            user_create_data.auth_pw = hashed_password
            
            # 새 사용자 생성
            new_user = await self.user_repository.create_user(db, user_create_data)
            
            logger.info(f"✅ 회원가입 완료: {new_user.email} (ID: {new_user.id})")
            
            return AuthResponse(
                success=True,
                message="회원가입이 완료되었습니다.",
                user_id=new_user.id,
                email=new_user.email,
                name=new_user.name,
                company_id=new_user.company_id
            )
            
        except Exception as e:
            logger.error(f"❌ 회원가입 처리 중 오류: {str(e)}")
            return AuthResponse(
                success=False,
                message=f"회원가입 처리 중 오류가 발생했습니다: {str(e)}"
            )
    
    # ==================== 로그아웃 기능 ====================
    
    async def logout_user(self, session_token: str) -> AuthResponse:
        """사용자 로그아웃 및 세션 제거"""
        try:
            logger.info(f"🚪 로그아웃 시도: {session_token}")
            
            # 세션 제거
            session_removed = await self.user_repository.remove_session(session_token)
            
            if session_removed:
                logger.info(f"✅ 로그아웃 완료: {session_token}")
                return AuthResponse(
                    success=True,
                    message="로그아웃되었습니다."
                )
            else:
                logger.warning(f"⚠️ 존재하지 않는 세션: {session_token}")
                return AuthResponse(
                    success=False,
                    message="존재하지 않는 세션입니다."
                )
                
        except Exception as e:
            logger.error(f"❌ 로그아웃 처리 중 오류: {str(e)}")
            return AuthResponse(
                success=False,
                message=f"로그아웃 처리 중 오류가 발생했습니다: {str(e)}"
            )
    
    # ==================== 프로필 조회 기능 ====================
    
    async def get_user_profile(self, db: AsyncSession, session_token: str) -> AuthResponse:
        """세션 토큰으로 사용자 프로필 조회"""
        try:
            logger.info(f"👤 프로필 조회 시도: {session_token}")
            
            # 세션 유효성 검증
            session_data = await self.user_repository.validate_session(session_token)
            if not session_data:
                logger.warning(f"❌ 유효하지 않은 세션: {session_token}")
                return AuthResponse(
                    success=False,
                    message="유효하지 않은 세션입니다."
                )
            
            # 사용자 정보 조회
            user = await self.user_repository.find_by_id(db, session_data["user_id"])
            if not user:
                logger.warning(f"❌ 사용자를 찾을 수 없음: {session_data['user_id']}")
                return AuthResponse(
                    success=False,
                    message="사용자 정보를 찾을 수 없습니다."
                )
            
            logger.info(f"✅ 프로필 조회 성공: {user.email}")
            
            return AuthResponse(
                success=True,
                message="프로필 조회가 완료되었습니다.",
                user_id=user.id,
                email=user.email,
                name=user.name,
                company_id=user.company_id
            )
            
        except Exception as e:
            logger.error(f"❌ 프로필 조회 중 오류: {str(e)}")
            return AuthResponse(
                success=False,
                message=f"프로필 조회 중 오류가 발생했습니다: {str(e)}"
            )
    
    # ==================== 토큰 검증 기능 ====================
    
    async def verify_access_token(self, token: str) -> Optional[Dict[str, Any]]:
        """액세스 토큰 검증"""
        try:
            token_data = self.jwt_manager.verify_token(token)
            return {
                "user_id": token_data.user_id,
                "email": token_data.email,
                "auth_id": token_data.auth_id
            }
        except Exception as e:
            logger.error(f"❌ 토큰 검증 실패: {str(e)}")
            return None
    
    # ==================== 보안 유틸리티 ====================
    
    async def _hash_password(self, password: str) -> str:
        """비밀번호 해시화 (SHA256)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    async def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        return await self._hash_password(plain_password) == hashed_password
    
    # ==================== 세션 관리 기능 ====================
    
    async def cleanup_expired_sessions(self) -> int:
        """만료된 세션 정리"""
        try:
            count = await self.user_repository.cleanup_expired_sessions()
            logger.info(f"ℹ️ 만료된 세션 {count}개 정리 완료")
            return count
        except Exception as e:
            logger.error(f"❌ 세션 정리 중 오류: {str(e)}")
            return 0
    
    async def get_active_sessions_count(self) -> int:
        """활성 세션 수 반환"""
        return self.user_repository.get_active_sessions_count()
    
    async def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 정보 반환"""
        return self.user_repository.get_session_info(session_id)
