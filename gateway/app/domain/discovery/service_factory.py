from typing import Optional
from fastapi import HTTPException
import httpx
import os
import logging

logger = logging.getLogger(__name__)

# 서비스 URL 매핑
SERVICE_URLS = {
    "auth-service": os.getenv("AUTH_SERVICE_URL", "https://auth-service-production-f2ef.up.railway.app"),
    "chatbot-service": os.getenv("CHATBOT_SERVICE_URL", "https://chatbot-service-production.up.railway.app"),
    "gri-service": os.getenv("GRI_SERVICE_URL", "https://gri-service-production.up.railway.app"),
    "materiality-service": os.getenv("MATERIALITY_SERVICE_URL", "https://materiality-service-production.up.railway.app"),
    "report-service": os.getenv("REPORT_SERVICE_URL", "https://report-service-production.up.railway.app"),
    "tcfd-service": os.getenv("TCFD_SERVICE_URL", "https://tcfd-service-production.up.railway.app"),
    "user-service": os.getenv("USER_SERVICE_URL", "https://user-service-production.up.railway.app"),
}

class ServiceProxyFactory:
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.base_url = SERVICE_URLS.get(service_name)
        
        if not self.base_url:
            raise ValueError(f"Service {service_name} not found in SERVICE_URLS")
        
        logger.info(f"👩🏻 Service URL: {self.base_url}")

    async def request(
        self,
        method: str,
        path: str,
        headers: Optional[dict] = None,
        body: Optional[str] = None
    ) -> httpx.Response:
        # 경로 구성 (서비스 prefix 포함)
        url = f"{self.base_url}{path}"
        logger.info(f"🎯🎯🎯 Requesting URL: {url}")
        
        # 기본 헤더 설정
        headers_dict = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # 외부 헤더가 있으면 병합
        if headers:
            headers_dict.update(headers)
        
        # host 헤더 제거 (프록시 요청시 문제 방지)
        if 'host' in headers_dict:
            del headers_dict['host']

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers_dict,
                    content=body,
                    timeout=30.0
                )
                logger.info(f"Response status: {response.status_code}")
                logger.info(f"Request URL: {url}")
                if body:
                    logger.info(f"Request body: {body}")
                return response
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

# 간단한 서비스 팩토리 (기존 코드와의 호환성을 위해)
class SimpleServiceFactory:
    def __init__(self):
        self.auth_service_url = os.getenv("AUTH_SERVICE_URL", "https://auth-service-production-f2ef.up.railway.app")
        logger.info(f"🔧 Auth Service URL: {self.auth_service_url}")
    
    async def forward_request(self, method: str, path: str, headers: dict = None, body: str = None) -> dict:
        """Auth Service로 요청을 전달"""
        try:
            # URL 구성
            url = f"{self.auth_service_url}{path}"
            logger.info(f"🎯 Auth Service로 전달: {method} {url}")
            
            # 헤더 준비
            request_headers = headers or {}
            if "host" in request_headers:
                del request_headers["host"]
            
            # 요청 파라미터
            request_kwargs = {
                "method": method,
                "url": url,
                "headers": request_headers,
                "timeout": 30.0
            }
            
            if body:
                request_kwargs["content"] = body
            
            # HTTP 요청 실행
            async with httpx.AsyncClient() as client:
                response = await client.request(**request_kwargs)
                
                logger.info(f"✅ Auth Service 응답: {response.status_code}")
                
                if response.status_code < 400:
                    try:
                        return {"status_code": response.status_code, "data": response.json()}
                    except Exception:
                        return {"status_code": response.status_code, "data": response.text}
                else:
                    return {
                        "error": True,
                        "status_code": response.status_code,
                        "detail": response.text
                    }
                    
        except Exception as e:
            logger.error(f"❌ Auth Service 요청 실패: {str(e)}")
            return {"error": True, "detail": str(e)}
