"""Risk Analysis Module"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class RiskAnalyzer:
    """Analyzer untuk menghitung risk score dan severity level"""

    # Severity weights
    SEVERITY_WEIGHTS = {
        "critical": 10,
        "high": 8,
        "medium": 5,
        "low": 2,
        "info": 1,
    }

    def __init__(self):
        """Initialize risk analyzer"""
        logger.info("RiskAnalyzer initialized")

    def calculate_risk_score(self, vulnerabilities: List[Dict]) -> float:
        """Calculate overall risk score
        
        Args:
            vulnerabilities: List of vulnerabilities
            
        Returns:
            Risk score (0-100)
        """
        if not vulnerabilities:
            return 0.0
        
        total_score = 0
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "info").lower()
            weight = self.SEVERITY_WEIGHTS.get(severity, 1)
            total_score += weight
        
        # Normalize to 0-100
        max_possible_score = len(vulnerabilities) * 10
        risk_score = min((total_score / max_possible_score) * 100, 100)
        
        logger.info(f"Calculated risk score: {risk_score}")
        return round(risk_score, 2)

    def categorize_risk(self, risk_score: float) -> str:
        """Categorize risk level based on score
        
        Args:
            risk_score: Risk score (0-100)
            
        Returns:
            Risk category
        """
        if risk_score >= 80:
            return "CRITICAL"
        elif risk_score >= 60:
            return "HIGH"
        elif risk_score >= 40:
            return "MEDIUM"
        elif risk_score >= 20:
            return "LOW"
        else:
            return "INFO"
