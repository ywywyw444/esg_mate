import httpx
import logging
import time
from typing import Dict, Optional, Any
from fastapi import HTTPException, Request
from fastapi.responses import Response, StreamingResponse
from urllib.parse import quote
import json

logger = logging.getLogger(__name__)

HOP_BY_HOP = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade"
}

class ProxyService:
    """프록시 서비스 클래스"""
    
    def __init__(self, service_discovery, timeout: int = 30):
        self.service_discovery = service_discovery
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def forward_request(
        self,
        service_name: str,
        path: str,
        method: str,
        headers: Dict,
        body: Optional[bytes] = None,
        query_params: Optional[Dict[str, Any]] = None
    ) -> Dict:
        """요청을 대상 서비스로 전달"""

        start_time = time.time()
        instance = None

        try:
            # 1) 서비스 인스턴스 조회
            instance = self.service_discovery.get_service_instance(service_name)
            if not instance:
                raise HTTPException(status_code=503, detail=f"Service {service_name} not available")

            # 2) 경로 안전 정리: 우발적 suffix(:json 등) 제거 + 세그먼트 인코딩 + 슬래시 보존
            raw_path = path or ""
            if ":" in raw_path:
                raw_path = raw_path.split(":", 1)[0]  # ':json' 같은 꼬리표 제거

            clean_path = raw_path.lstrip("/")
            encoded_segments = [quote(seg, safe="@:$,;~()[]!*-_.") for seg in clean_path.split("/") if seg != ""]
            base_url = instance.url.rstrip("/")
            target_url = f"{base_url}/{'/'.join(encoded_segments)}" if encoded_segments else base_url

            # 3) 헤더 정리 (hop-by-hop/host/content-length 제거)
            clean_headers = {
                k: v for k, v in headers.items()
                if k.lower() not in HOP_BY_HOP | {"host", "content-length"}
            }

            # 4) 요청 전달 (쿼리는 httpx의 params로 넘겨 자동 인코딩)
            logger.info(f"Forwarding {method} request to {target_url}")
            response = await self.client.request(
                method=method,
                url=target_url,
                headers=clean_headers,
                content=body if method not in ("GET", "HEAD") else None,
                params=query_params  # ← 수동 문자열 조립 금지, 자동 인코딩
            )

            response_time = time.time() - start_time
            logger.info(f"Response from {service_name}: {response.status_code} ({response_time:.3f}s)")

            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.content,
                "service": service_name,
                "target_url": str(response.request.url),
                "response_time": response_time,
                "instance": f"{getattr(instance, 'host', '')}:{getattr(instance, 'port', '')}".strip(":")
            }

        except httpx.TimeoutException:
            logger.error(f"Timeout error for service {service_name}")
            raise HTTPException(status_code=504, detail=f"Service {service_name} timeout")

        except httpx.ConnectError:
            logger.error(f"Connection error for service {service_name}")
            raise HTTPException(status_code=503, detail=f"Service {service_name} connection failed")

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Unexpected error forwarding request to {service_name}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

        finally:
            if instance:
                self.service_discovery.release_instance(service_name, instance)

    async def handle_request(self, request: Request, service_name: str, path: str) -> Response:
        """요청 처리 및 응답 반환"""
        body = await request.body()

        # FastAPI의 QueryParams는 다중값 보존됨 → httpx params에 그대로 전달
        query_params = request.query_params

        result = await self.forward_request(
            service_name=service_name,
            path=f"/{path}",
            method=request.method,
            headers=dict(request.headers),
            body=body,
            query_params=query_params
        )

        # 응답 헤더 정리 + CORS 보강
        resp_headers = {
            k: v for k, v in result["headers"].items()
            if k.lower() not in HOP_BY_HOP | {"content-length"}  # 길이는 FastAPI가 재계산
        }
        resp_headers["Access-Control-Allow-Origin"] = "*"
        resp_headers["Access-Control-Allow-Methods"] = "*"
        resp_headers["Access-Control-Allow-Headers"] = "*"
        resp_headers["X-Gateway-Service"] = service_name
        resp_headers["X-Gateway-Instance"] = result["instance"]
        resp_headers["X-Gateway-Response-Time"] = f"{result['response_time']:.3f}s"

        # 단순 버퍼링된 응답이면 Response로 반환
        return Response(
            content=result["content"],
            status_code=result["status_code"],
            headers=resp_headers,
            media_type=result["headers"].get("content-type")
        )

    async def health_check_service(self, service_name: str) -> Dict:
        """서비스 헬스 체크"""
        try:
            result = await self.forward_request(
                service_name=service_name,
                path="/health",
                method="GET",
                headers={"Content-Type": "application/json"},
                body=None
            )
            return {
                "service": service_name,
                "status": "healthy" if result["status_code"] == 200 else "unhealthy",
                "response_time": result["response_time"],
                "instance": result["instance"]
            }
        except Exception as e:
            return {"service": service_name, "status": "unhealthy", "error": str(e)}

    async def close(self):
        """리소스 정리"""
        await self.client.aclose()
