"""
JWT 유틸리티 - 토큰 생성, 검증, 세션 관리
"""
import os
import jwt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from app.domain.user_schema import TokenData, SessionData

logger = logging.getLogger("auth_service_jwt")

# JWT 설정
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key_here")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class JWTManager:
    """JWT 토큰 관리자"""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """액세스 토큰 생성"""
        try:
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
            
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
            
            logger.info(f"✅ JWT 토큰 생성 완료: {data.get('email', 'N/A')}")
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"❌ JWT 토큰 생성 실패: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="토큰 생성 중 오류가 발생했습니다."
            )
    
    @staticmethod
    def verify_token(token: str) -> TokenData:
        """토큰 검증 및 데이터 추출"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            
            # 토큰 만료 확인
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="토큰이 만료되었습니다."
                )
            
            token_data = TokenData(
                user_id=payload.get("user_id"),
                email=payload.get("email"),
                auth_id=payload.get("auth_id")
            )
            
            logger.info(f"✅ JWT 토큰 검증 성공: {token_data.email}")
            return token_data
            
        except jwt.PyJWTError as e:
            logger.error(f"❌ JWT 토큰 검증 실패: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 토큰입니다."
            )
        except Exception as e:
            logger.error(f"❌ 토큰 검증 중 오류: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="토큰 검증 중 오류가 발생했습니다."
            )
    
    @staticmethod
    def create_session_data(user_id: int, email: str, auth_id: str, company_id: str) -> SessionData:
        """세션 데이터 생성"""
        exp = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        
        return SessionData(
            user_id=user_id,
            email=email,
            auth_id=auth_id,
            company_id=company_id,
            exp=exp
        )
    
    @staticmethod
    def extract_token_from_header(authorization: Optional[str]) -> str:
        """Authorization 헤더에서 토큰 추출"""
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization 헤더가 없습니다."
            )
        
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer 토큰 형식이 아닙니다."
            )
        
        return authorization.split(" ")[1]
