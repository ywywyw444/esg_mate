"""
Auth Service Models
"""
from sqlalchemy import Column, String, Integer, Text
from .database.database import Base

class User(Base):
    """사용자 테이블"""
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
