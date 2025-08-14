"""
User Repository - 인증 데이터 관리 및 세션 관리
"""
import logging
import asyncio
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from app.domain.user_schema import UserModel, UserEntity, UserCreateEntity, UserUpdateEntity

logger = logging.getLogger("auth_service_repository")

class UserRepository:
    """사용자 리포지토리 - 인증 데이터 관리 및 세션 관리"""
    
    def __init__(self):
        self._active_sessions: Dict[str, Dict[str, Any]] = {}
        self._session_lock = asyncio.Lock()
    
    # ==================== 사용자 조회 ====================
    
    @staticmethod
    async def find_by_email(db: AsyncSession, email: str) -> Optional[UserModel]:
        """이메일로 사용자 조회"""
        try:
            query = select(UserModel).where(UserModel.email == email)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                logger.info(f"✅ 이메일로 사용자 조회 성공: {email}")
            else:
                logger.info(f"ℹ️ 이메일로 사용자 조회 실패: {email}")
            
            return user
            
        except Exception as e:
            logger.error(f"❌ 이메일로 사용자 조회 중 오류: {str(e)}")
            raise
    
    @staticmethod
    async def find_by_auth_id(db: AsyncSession, auth_id: str) -> Optional[UserModel]:
        """인증 ID로 사용자 조회"""
        try:
            query = select(UserModel).where(UserModel.auth_id == auth_id)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                logger.info(f"✅ 인증 ID로 사용자 조회 성공: {auth_id}")
            else:
                logger.info(f"ℹ️ 인증 ID로 사용자 조회 실패: {auth_id}")
            
            return user
            
        except Exception as e:
            logger.error(f"❌ 인증 ID로 사용자 조회 중 오류: {str(e)}")
            raise
    
    @staticmethod
    async def find_by_id(db: AsyncSession, user_id: int) -> Optional[UserModel]:
        """사용자 ID로 사용자 조회"""
        try:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                logger.info(f"✅ 사용자 ID로 조회 성공: {user_id}")
            else:
                logger.info(f"ℹ️ 사용자 ID로 조회 실패: {user_id}")
            
            return user
            
        except Exception as e:
            logger.error(f"❌ 사용자 ID로 조회 중 오류: {str(e)}")
            raise
    
    @staticmethod
    async def find_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """모든 사용자 조회 (페이지네이션)"""
        try:
            query = select(UserModel).offset(skip).limit(limit)
            result = await db.execute(query)
            users = result.scalars().all()
            
            logger.info(f"✅ 전체 사용자 조회 성공: {len(users)}명")
            return users
            
        except Exception as e:
            logger.error(f"❌ 전체 사용자 조회 중 오류: {str(e)}")
            raise
    
    # ==================== 사용자 생성/수정/삭제 ====================
    
    @staticmethod
    async def create_user(db: AsyncSession, user_data: UserCreateEntity) -> UserModel:
        """새 사용자 생성"""
        try:
            new_user = UserModel(
                company_id=user_data.company_id,
                industry=user_data.industry,
                email=user_data.email,
                name=user_data.name,
                age=user_data.age,
                auth_id=user_data.auth_id,
                auth_pw=user_data.auth_pw
            )
            
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            
            logger.info(f"✅ 새 사용자 생성 완료: {new_user.email} (ID: {new_user.id})")
            return new_user
            
        except Exception as e:
            await db.rollback()
            logger.error(f"❌ 사용자 생성 중 오류: {str(e)}")
            raise
    
    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdateEntity) -> Optional[UserModel]:
        """사용자 정보 수정"""
        try:
            update_data = user_data.dict(exclude_unset=True)
            if not update_data:
                return None
            
            query = update(UserModel).where(UserModel.id == user_id).values(**update_data)
            await db.execute(query)
            await db.commit()
            
            # 수정된 사용자 조회
            updated_user = await UserRepository.find_by_id(db, user_id)
            
            if updated_user:
                logger.info(f"✅ 사용자 정보 수정 완료: {user_id}")
            else:
                logger.warning(f"⚠️ 수정된 사용자를 찾을 수 없음: {user_id}")
            
            return updated_user
            
        except Exception as e:
            await db.rollback()
            logger.error(f"❌ 사용자 정보 수정 중 오류: {str(e)}")
            raise
    
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """사용자 삭제"""
        try:
            query = delete(UserModel).where(UserModel.id == user_id)
            result = await db.execute(query)
            await db.commit()
            
            if result.rowcount > 0:
                logger.info(f"✅ 사용자 삭제 완료: {user_id}")
                return True
            else:
                logger.warning(f"⚠️ 삭제할 사용자를 찾을 수 없음: {user_id}")
                return False
                
        except Exception as e:
            await db.rollback()
            logger.error(f"❌ 사용자 삭제 중 오류: {str(e)}")
            raise
    
    # ==================== 세션 관리 ====================
    
    async def create_session(self, user_id: int, email: str, auth_id: str, company_id: str) -> str:
        """새 세션 생성"""
        async with self._session_lock:
            try:
                # 기존 세션 정리 (같은 사용자의 경우)
                await self._cleanup_user_sessions(user_id)
                
                # 새 세션 생성
                session_id = f"session_{user_id}_{asyncio.get_event_loop().time()}"
                session_data = {
                    "user_id": user_id,
                    "email": email,
                    "auth_id": auth_id,
                    "company_id": company_id,
                    "created_at": asyncio.get_event_loop().time(),
                    "last_activity": asyncio.get_event_loop().time()
                }
                
                self._active_sessions[session_id] = session_data
                
                logger.info(f"✅ 새 세션 생성: {session_id} (사용자: {email})")
                return session_id
                
            except Exception as e:
                logger.error(f"❌ 세션 생성 중 오류: {str(e)}")
                raise
    
    async def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 유효성 검증"""
        async with self._session_lock:
            try:
                if session_id not in self._active_sessions:
                    logger.warning(f"⚠️ 존재하지 않는 세션: {session_id}")
                    return None
                
                session_data = self._active_sessions[session_id]
                current_time = asyncio.get_event_loop().time()
                
                # 세션 만료 확인 (30분)
                if current_time - session_data["last_activity"] > 1800:  # 30분
                    await self._remove_session(session_id)
                    logger.info(f"ℹ️ 만료된 세션 제거: {session_id}")
                    return None
                
                # 마지막 활동 시간 업데이트
                session_data["last_activity"] = current_time
                
                logger.info(f"✅ 세션 유효성 검증 성공: {session_id}")
                return session_data
                
            except Exception as e:
                logger.error(f"❌ 세션 유효성 검증 중 오류: {str(e)}")
                return None
    
    async def remove_session(self, session_id: str) -> bool:
        """세션 제거"""
        async with self._session_lock:
            return await self._remove_session(session_id)
    
    async def _remove_session(self, session_id: str) -> bool:
        """세션 제거 (내부 메서드)"""
        try:
            if session_id in self._active_sessions:
                del self._active_sessions[session_id]
                logger.info(f"✅ 세션 제거 완료: {session_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"❌ 세션 제거 중 오류: {str(e)}")
            return False
    
    async def _cleanup_user_sessions(self, user_id: int) -> None:
        """사용자의 기존 세션 정리"""
        try:
            sessions_to_remove = [
                session_id for session_id, session_data in self._active_sessions.items()
                if session_data["user_id"] == user_id
            ]
            
            for session_id in sessions_to_remove:
                await self._remove_session(session_id)
                
            if sessions_to_remove:
                logger.info(f"ℹ️ 사용자 {user_id}의 기존 세션 {len(sessions_to_remove)}개 정리 완료")
                
        except Exception as e:
            logger.error(f"❌ 사용자 세션 정리 중 오류: {str(e)}")
    
    async def cleanup_expired_sessions(self) -> int:
        """만료된 세션 정리"""
        async with self._session_lock:
            try:
                current_time = asyncio.get_event_loop().time()
                expired_sessions = [
                    session_id for session_id, session_data in self._active_sessions.items()
                    if current_time - session_data["last_activity"] > 1800  # 30분
                ]
                
                for session_id in expired_sessions:
                    await self._remove_session(session_id)
                
                if expired_sessions:
                    logger.info(f"ℹ️ 만료된 세션 {len(expired_sessions)}개 정리 완료")
                
                return len(expired_sessions)
                
            except Exception as e:
                logger.error(f"❌ 만료된 세션 정리 중 오류: {str(e)}")
                return 0
    
    def get_active_sessions_count(self) -> int:
        """활성 세션 수 반환"""
        return len(self._active_sessions)
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """세션 정보 반환 (읽기 전용)"""
        return self._active_sessions.get(session_id)
