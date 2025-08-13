# gateway/app/router/main.py
from fastapi import FastAPI
from app.www.jwt_auth_middleware import AuthMiddleware
from app.domain.discovery.service_discovery import ServiceDiscovery

from app.www.proxy import router as proxy_router  # ← 추가

app = FastAPI()

# 서비스 디스커버리 준비
@app.on_event("startup")
async def _startup():
    app.state.service_discovery = ServiceDiscovery()

# 문서/헬스 등은 미들웨어에서 패스
PASS_PATHS = {"/", "/health", "/health/db", "/docs", "/redoc", "/openapi.json"}

class _AuthBypass(AuthMiddleware):
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope.get("path") in PASS_PATHS:
            return await self.app(scope, receive, send)
        return await super().__call__(scope, receive, send)

app.add_middleware(_AuthBypass)

# 프록시 라우터 등록 (스키마 숨김 권장)
app.include_router(proxy_router, include_in_schema=False)
