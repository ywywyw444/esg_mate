import logging
from typing import Any, Dict, Union
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

class ResponseFactory:
    """응답 생성 팩토리 클래스"""
    
    @staticmethod
    def create_response(response_data: Any) -> JSONResponse:
        """응답 데이터를 기반으로 적절한 JSONResponse 생성"""
        try:
            # response_data가 dict인 경우
            if isinstance(response_data, dict):
                # 에러 응답인 경우
                if response_data.get("error"):
                    status_code = response_data.get("status_code", 500)
                    return JSONResponse(
                        content=response_data,
                        status_code=status_code
                    )
                # 성공 응답인 경우
                else:
                    return JSONResponse(
                        content=response_data,
                        status_code=200
                    )
            
            # response_data가 다른 타입인 경우
            else:
                return JSONResponse(
                    content={"data": response_data},
                    status_code=200
                )
                
        except Exception as e:
            logger.error(f"ResponseFactory 오류: {str(e)}")
            return JSONResponse(
                content={"error": True, "detail": "응답 생성 중 오류 발생"},
                status_code=500
            ) 