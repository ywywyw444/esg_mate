"""
Auth Service Database Configuration - Railway PostgreSQL 연결 최적화
"""
import os
import logging
import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from sqlalchemy.pool import QueuePool

logger = logging.getLogger("auth_service_db")

# Railway PostgreSQL 연결 설정 (필수)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("❌ DATABASE_URL 환경변수가 설정되지 않았습니다.")
    raise ValueError("DATABASE_URL 환경변수를 설정해주세요.")

# Railway PostgreSQL URL을 asyncpg용으로 변환
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "asyncpg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

logger.info(f"✅ Railway PostgreSQL 연결 설정 완료: {DATABASE_URL.split('@')[0]}@***")

# 연결 풀 설정 최적화
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "30"))
POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))
POOL_PRE_PING = os.getenv("DB_POOL_PRE_PING", "true").lower() == "true"

# 비동기 엔진 생성 (연결 풀 최적화)
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DB_ECHO", "false").lower() == "true",
    pool_pre_ping=POOL_PRE_PING,
    pool_recycle=POOL_RECYCLE,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    poolclass=QueuePool,
    # Railway 환경 최적화 설정
    connect_args={
        "server_settings": {
            "application_name": "auth_service",
            "timezone": "UTC"
        },
        "command_timeout": 60,
        "statement_timeout": 30000,  # 30초
        "query_timeout": 30000,      # 30초
    }
)

# 비동기 세션 팩토리
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base 클래스
Base = declarative_base()

# DB 세션 의존성
async def get_db():
    """데이터베이스 세션 의존성"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# 연결 풀 상태 모니터링
async def get_pool_status():
    """연결 풀 상태 조회"""
    try:
        pool = engine.pool
        return {
            "pool_size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "invalid": pool.invalid()
        }
    except Exception as e:
        logger.error(f"❌ 연결 풀 상태 조회 실패: {str(e)}")
        return {"error": str(e)}

# 연결 테스트 함수
async def test_connection():
    """데이터베이스 연결을 테스트합니다."""
    try:
        async with engine.begin() as conn:
            # 연결 테스트 쿼리
            result = await conn.execute(text("SELECT 1 as test, version() as db_version"))
            row = result.fetchone()
            
            logger.info(f"✅ 데이터베이스 연결 성공")
            logger.info(f"📊 데이터베이스 버전: {row.db_version}")
            
            # 연결 풀 상태 확인
            pool_status = await get_pool_status()
            logger.info(f"🔗 연결 풀 상태: {pool_status}")
            
            return True
            
    except Exception as e:
        logger.error(f"❌ 데이터베이스 연결 실패: {str(e)}")
        return False

# 테이블 생성 함수 (존재하지 않는 경우에만 생성, 데이터 보호)
async def create_tables():
    """필요한 테이블을 생성합니다."""
    try:
        async with engine.begin() as conn:
            # 테이블 존재 여부 확인
            result = await conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'user'
                );
            """))
            table_exists = result.scalar()

            if not table_exists:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("✅ 데이터베이스 테이블이 생성되었습니다.")
            else:
                # 기존 데이터 개수 확인
                count_result = await conn.execute(text("SELECT COUNT(*) FROM user"))
                user_count = count_result.scalar()
                logger.info(f"ℹ️ 데이터베이스 테이블이 이미 존재합니다. (기존 사용자: {user_count}명)")
                
    except Exception as e:
        logger.error(f"❌ 테이블 생성 중 오류: {str(e)}")
        raise

# 연결 풀 정리
async def cleanup_pool():
    """연결 풀 정리"""
    try:
        await engine.dispose()
        logger.info("✅ 데이터베이스 연결 풀이 정리되었습니다.")
    except Exception as e:
        logger.error(f"❌ 연결 풀 정리 중 오류: {str(e)}")

# 주기적 연결 풀 상태 체크
async def monitor_pool_health():
    """연결 풀 상태를 주기적으로 모니터링"""
    while True:
        try:
            pool_status = await get_pool_status()
            logger.info(f"🔍 연결 풀 상태 모니터링: {pool_status}")
            
            # 연결 풀 상태가 비정상인 경우 경고
            if pool_status.get("checked_out", 0) > POOL_SIZE * 0.8:
                logger.warning(f"⚠️ 연결 풀 사용률이 높습니다: {pool_status}")
            
            # 5분마다 체크
            await asyncio.sleep(300)
            
        except Exception as e:
            logger.error(f"❌ 연결 풀 모니터링 중 오류: {str(e)}")
            await asyncio.sleep(60)  # 오류 시 1분 후 재시도

# 애플리케이션 시작 시 초기화
async def initialize_database():
    """데이터베이스 초기화"""
    try:
        logger.info("🚀 데이터베이스 초기화 시작...")
        
        # 연결 테스트
        if not await test_connection():
            raise Exception("데이터베이스 연결 실패")
        
        # 테이블 생성
        await create_tables()
        
        # 연결 풀 모니터링 시작
        asyncio.create_task(monitor_pool_health())
        
        logger.info("✅ 데이터베이스 초기화 완료")
        
    except Exception as e:
        logger.error(f"❌ 데이터베이스 초기화 실패: {str(e)}")
        raise

# 애플리케이션 종료 시 정리
async def shutdown_database():
    """데이터베이스 정리"""
    try:
        logger.info("🛑 데이터베이스 정리 시작...")
        await cleanup_pool()
        logger.info("✅ 데이터베이스 정리 완료")
    except Exception as e:
        logger.error(f"❌ 데이터베이스 정리 중 오류: {str(e)}")
