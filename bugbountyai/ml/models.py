"""ML Models untuk vulnerability prediction"""

import logging
from typing import List, Dict, Any
import numpy as np

logger = logging.getLogger(__name__)


class MLVulnerabilityPredictor:
    """ML model untuk memprediksi vulnerabilities"""

    def __init__(self):
        """Initialize ML predictor"""
        self.model_name = "VulnerabilityPredictor-v1"
        logger.info(f"MLVulnerabilityPredictor initialized: {self.model_name}")

    def predict(self, vulnerabilities: List[Dict]) -> List[Dict[str, Any]]:
        """Predict vulnerability severity dan impact
        
        Args:
            vulnerabilities: List of detected vulnerabilities
            
        Returns:
            List of predictions dengan confidence scores
        """
        predictions = []
        
        for vuln in vulnerabilities:
            prediction = {
                "vulnerability_type": vuln.get("type"),
                "original_severity": vuln.get("severity"),
                "predicted_severity": self._predict_severity(vuln),
                "exploitability_score": self._predict_exploitability(vuln),
                "confidence": self._calculate_confidence(vuln),
            }
            predictions.append(prediction)
        
        logger.info(f"Generated {len(predictions)} predictions")
        return predictions

    @staticmethod
    def _predict_severity(vuln: Dict) -> str:
        """Predict severity level"""
        # Simplified prediction logic
        return vuln.get("severity", "medium")

    @staticmethod
    def _predict_exploitability(vuln: Dict) -> float:
        """Predict exploitability score (0-1)"""
        # Simplified exploitability prediction
        severity_to_exploitability = {
            "critical": 0.95,
            "high": 0.85,
            "medium": 0.65,
            "low": 0.35,
            "info": 0.10,
        }
        severity = vuln.get("severity", "medium").lower()
        return severity_to_exploitability.get(severity, 0.5)

    @staticmethod
    def _calculate_confidence(vuln: Dict) -> float:
        """Calculate prediction confidence (0-1)"""
        # Simplified confidence calculation
        return 0.85
