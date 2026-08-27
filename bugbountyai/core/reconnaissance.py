"""Reconnaissance Module untuk gathering target information"""

import logging
from typing import Dict, Any
import socket
import requests
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ReconnaissanceModule:
    """Module untuk mengumpulkan informasi tentang target"""

    def __init__(self):
        """Initialize reconnaissance module"""
        self.session = requests.Session()
        logger.info("ReconnaissanceModule initialized")

    def gather_info(self, target_url: str) -> Dict[str, Any]:
        """Gather informasi tentang target
        
        Args:
            target_url: URL target
            
        Returns:
            Dictionary berisi informasi target
        """
        info = {
            "target_url": target_url,
            "domain_info": {},
            "technology_stack": [],
            "endpoints": [],
            "subdomains": [],
        }
        
        try:
            parsed_url = urlparse(target_url)
            
            # Get domain info
            info["domain_info"] = self._get_domain_info(parsed_url.netloc)
            
            # Detect technology stack
            info["technology_stack"] = self._detect_technologies(target_url)
            
            # Find endpoints
            info["endpoints"] = self._find_endpoints(target_url)
            
            logger.info(f"Reconnaissance completed for {target_url}")
            
        except Exception as e:
            logger.error(f"Error during reconnaissance: {str(e)}")
        
        return info

    def _get_domain_info(self, domain: str) -> Dict[str, Any]:
        """Get domain information"""
        info = {
            "domain": domain,
            "ip_address": None,
            "hostname": None,
        }
        
        try:
            info["ip_address"] = socket.gethostbyname(domain)
            info["hostname"] = socket.getfqdn(domain)
        except Exception as e:
            logger.warning(f"Could not resolve domain: {str(e)}")
        
        return info

    def _detect_technologies(self, target_url: str) -> list:
        """Detect technologies used by target"""
        technologies = []
        
        try:
            response = self.session.get(target_url, timeout=10)
            headers = response.headers
            content = response.text
            
            # Detect by headers
            if "Server" in headers:
                technologies.append({"name": "Server", "value": headers["Server"]})
            
            if "X-Powered-By" in headers:
                technologies.append({"name": "Powered-By", "value": headers["X-Powered-By"]})
            
            # Detect by content patterns
            if "react" in content.lower():
                technologies.append({"name": "Frontend", "value": "React"})
            
            if "angular" in content.lower():
                technologies.append({"name": "Frontend", "value": "Angular"})
            
            if "vue" in content.lower():
                technologies.append({"name": "Frontend", "value": "Vue.js"})
        
        except Exception as e:
            logger.warning(f"Error detecting technologies: {str(e)}")
        
        return technologies

    def _find_endpoints(self, target_url: str) -> list:
        """Find accessible endpoints"""
        endpoints = []
        common_paths = [
            "/api",
            "/admin",
            "/login",
            "/register",
            "/.git",
            "/config",
            "/robots.txt",
            "/sitemap.xml",
        ]
        
        try:
            for path in common_paths:
                try:
                    response = self.session.head(
                        target_url.rstrip("/") + path,
                        timeout=5,
                        allow_redirects=False,
                    )
                    if response.status_code < 400:
                        endpoints.append({"path": path, "status": response.status_code})
                except:
                    pass
        
        except Exception as e:
            logger.warning(f"Error finding endpoints: {str(e)}")
        
        return endpoints
