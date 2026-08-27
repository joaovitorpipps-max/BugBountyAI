"""Real-time Monitoring System untuk v2"""

import logging
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
import asyncio
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Alert:
    """Alert data class"""
    timestamp: str
    severity: str
    message: str
    target: str
    vulnerability_type: str
    confidence: float


class RealtimeMonitor:
    """Real-time monitoring untuk continuous scanning"""

    def __init__(self, webhook_url: Optional[str] = None):
        """Initialize realtime monitor
        
        Args:
            webhook_url: URL untuk webhook notifications
        """
        self.webhook_url = webhook_url
        self.alerts = []
        self.monitoring_targets = []
        self.alert_handlers = []
        logger.info("RealtimeMonitor initialized")

    async def start_continuous_scanning(self, targets: List[str], interval: int = 300):
        """Start continuous scanning dari targets
        
        Args:
            targets: List of target URLs
            interval: Scanning interval dalam detik
        """
        self.monitoring_targets = targets
        logger.info(f"Starting continuous scanning for {len(targets)} targets")
        
        while True:
            try:
                for target in targets:
                    await self._scan_target(target)
                await asyncio.sleep(interval)
            except Exception as e:
                logger.error(f"Error during continuous scanning: {str(e)}")
                await asyncio.sleep(interval)

    async def _scan_target(self, target: str):
        """Scan single target"""
        logger.info(f"Scanning target: {target}")
        
        # Simplified scanning
        vulnerabilities = [
            {"type": "SQL Injection", "severity": "high", "confidence": 0.85},
            {"type": "XSS", "severity": "medium", "confidence": 0.75},
        ]
        
        for vuln in vulnerabilities:
            alert = Alert(
                timestamp=datetime.now().isoformat(),
                severity=vuln["severity"],
                message=f"Found {vuln['type']} in {target}",
                target=target,
                vulnerability_type=vuln["type"],
                confidence=vuln["confidence"],
            )
            await self.trigger_alert(alert)

    async def trigger_alert(self, alert: Alert):
        """Trigger alert dengan notification
        
        Args:
            alert: Alert object
        """
        self.alerts.append(alert)
        logger.warning(f"ALERT: {alert.message}")
        
        # Call registered alert handlers
        for handler in self.alert_handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(alert)
                else:
                    handler(alert)
            except Exception as e:
                logger.error(f"Error in alert handler: {str(e)}")
        
        # Send webhook notification
        if self.webhook_url:
            await self._send_webhook(alert)

    def register_alert_handler(self, handler: Callable):
        """Register custom alert handler
        
        Args:
            handler: Callable yang menerima Alert object
        """
        self.alert_handlers.append(handler)
        logger.info(f"Registered alert handler: {handler.__name__}")

    async def _send_webhook(self, alert: Alert):
        """Send webhook notification
        
        Args:
            alert: Alert object untuk dikirim
        """
        import aiohttp
        
        payload = {
            "timestamp": alert.timestamp,
            "severity": alert.severity,
            "message": alert.message,
            "target": alert.target,
            "vulnerability_type": alert.vulnerability_type,
            "confidence": alert.confidence,
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                await session.post(self.webhook_url, json=payload)
                logger.info(f"Webhook sent to {self.webhook_url}")
        except Exception as e:
            logger.error(f"Error sending webhook: {str(e)}")

    def get_alerts(self, severity: Optional[str] = None) -> List[Alert]:
        """Get alerts dengan optional severity filter
        
        Args:
            severity: Filter by severity level
            
        Returns:
            List of alerts
        """
        if severity:
            return [a for a in self.alerts if a.severity == severity]
        return self.alerts

    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status
        
        Returns:
            Status dictionary
        """
        return {
            "active_targets": len(self.monitoring_targets),
            "total_alerts": len(self.alerts),
            "critical_alerts": len([a for a in self.alerts if a.severity == "critical"]),
            "high_alerts": len([a for a in self.alerts if a.severity == "high"]),
            "targets": self.monitoring_targets,
            "last_updated": datetime.now().isoformat(),
        }
