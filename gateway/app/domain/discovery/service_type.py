from enum import Enum

class ServiceType(str, Enum):
    """서비스 타입 enum"""
    CHATBOT = "chatbot"
    GRI = "gri"
    MATERIALITY = "materiality"
    REPORT = "report"
    TCFD = "tcfd"
    USER = "user"
    AUTH = "auth" 