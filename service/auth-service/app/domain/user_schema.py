"""
User Schema - Pydantic BaseModel 및 SQLAlchemy 모델 정의
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text
from app.common.database.database import Base

# ==================== Pydantic BaseModel (Schema) ====================

class LoginRequest(BaseModel):
    """로그인 요청 스키마"""
    auth_id: str = Field(..., description="사용자 인증 ID", min_length=1)
    auth_pw: str = Field(..., description="사용자 비밀번호", min_length=1)

class SignupRequest(BaseModel):
    """회원가입 요청 스키마"""
    company_id: str = Field(..., description="회사 ID", min_length=1)
    industry: str = Field(..., description="산업 분야", min_length=1)
    email: str = Field(..., description="이메일 주소", pattern=r"^[^@]+@[^@]+\.[^@]+$")
    name: str = Field(..., description="사용자 이름", min_length=1)
    age: str = Field(..., description="나이", min_length=1)
    auth_id: str = Field(..., description="인증 ID", min_length=1)
    auth_pw: str = Field(..., description="인증 비밀번호", min_length=6)

class LogoutRequest(BaseModel):
    """로그아웃 요청 스키마"""
    session_token: Optional[str] = Field(None, description="세션 토큰")

# ==================== 응답 스키마 ====================

class AuthResponse(BaseModel):
    """인증 응답 스키마"""
    success: bool = Field(..., description="요청 성공 여부")
    message: str = Field(..., description="응답 메시지")
    user_id: Optional[int] = Field(None, description="사용자 ID")
    email: Optional[str] = Field(None, description="이메일 주소")
    name: Optional[str] = Field(None, description="사용자 이름")
    company_id: Optional[str] = Field(None, description="회사 ID")
    token: Optional[str] = Field(None, description="JWT 토큰")

class UserProfileResponse(BaseModel):
    """사용자 프로필 응답 스키마"""
    success: bool = Field(..., description="요청 성공 여부")
    message: str = Field(..., description="응답 메시지")
    user: Optional[dict] = Field(None, description="사용자 정보")

# ==================== 엔티티 스키마 ====================

class UserEntity(BaseModel):
    """사용자 엔티티 스키마"""
    id: Optional[int] = None
    company_id: str
    industry: str
    email: str
    name: str
    age: str
    auth_id: str
    auth_pw: Optional[str] = None  # 응답 시에는 비밀번호 제외

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserCreateEntity(BaseModel):
    """사용자 생성 엔티티 스키마"""
    company_id: str
    industry: str
    email: str
    name: str
    age: str
    auth_id: str
    auth_pw: str

class UserUpdateEntity(BaseModel):
    """사용자 수정 엔티티 스키마"""
    company_id: Optional[str] = None
    industry: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    age: Optional[str] = None
    auth_pw: Optional[str] = None

# ==================== 세션 스키마 ====================

class SessionData(BaseModel):
    """세션 데이터 스키마"""
    user_id: int
    email: str
    auth_id: str
    company_id: str
    exp: datetime

class TokenData(BaseModel):
    """토큰 데이터 스키마"""
    user_id: Optional[int] = None
    email: Optional[str] = None
    auth_id: Optional[str] = None

# ==================== SQLAlchemy 모델 (Database Model) ====================

class UserModel(Base):
    """사용자 데이터베이스 모델 - SQLAlchemy Base 클래스로 DB 연결"""
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company_id = Column(Text, nullable=False, comment="회사 ID")
    industry = Column(Text, nullable=False, comment="산업")
    email = Column(Text, nullable=False, unique=True, index=True, comment="이메일")
    name = Column(Text, nullable=False, comment="이름")
    age = Column(Text, nullable=False, comment="나이")
    auth_id = Column(Text, nullable=False, unique=True, index=True, comment="인증 ID")
    auth_pw = Column(Text, nullable=False, comment="인증 비밀번호 (해시)")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', company_id='{self.company_id}')>"

    def to_entity(self) -> UserEntity:
        """SQLAlchemy 모델을 Pydantic 엔티티로 변환"""
        return UserEntity(
            id=self.id,
            company_id=self.company_id,
            industry=self.industry,
            email=self.email,
            name=self.name,
            age=self.age,
            auth_id=self.auth_id
            # auth_pw는 보안상 제외
        )

    @classmethod
    def from_entity(cls, entity: UserCreateEntity) -> 'UserModel':
        """Pydantic 엔티티로부터 SQLAlchemy 모델 생성"""
        return cls(
            company_id=entity.company_id,
            industry=entity.industry,
            email=entity.email,
            name=entity.name,
            age=entity.age,
            auth_id=entity.auth_id,
            auth_pw=entity.auth_pw
        )
