from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # Gateway 설정
    GATEWAY_HOST: str = "0.0.0.0"
    GATEWAY_PORT: int = 8080
    GATEWAY_RELOAD: bool = True
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    
    # 요청 설정
    REQUEST_TIMEOUT: int = 30
    HEALTH_CHECK_INTERVAL: int = 30
    
    # CORS 설정 - 단순 문자열로 변경
    CORS_ORIGINS: str = "*"  # 모든 origin 허용
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "*"
    CORS_ALLOW_HEADERS: str = "*"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # 추가 환경변수 무시 