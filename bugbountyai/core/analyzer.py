"""Main BugBountyAI Analyzer Module"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from bugbountyai.core.scanner import VulnerabilityScanner
from bugbountyai.core.reconnaissance import ReconnaissanceModule
from bugbountyai.core.risk_analyzer import RiskAnalyzer
from bugbountyai.ml.models import MLVulnerabilityPredictor
from bugbountyai.reporting.report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class BugBountyAnalyzer:
    """Main analyzer untuk bug bounty scanning dan reporting"""

    def __init__(self, api_key: str, config: Optional[Dict] = None):
        """Initialize analyzer dengan API key dan config"""
        self.api_key = api_key
        self.config = config or {}
        
        # Initialize modules
        self.scanner = VulnerabilityScanner()
        self.recon = ReconnaissanceModule()
        self.risk_analyzer = RiskAnalyzer()
        self.ml_predictor = MLVulnerabilityPredictor()
        self.report_generator = ReportGenerator()
        
        logger.info("BugBountyAnalyzer initialized successfully")

    def analyze_target(self, target_url: str, deep_scan: bool = False) -> Dict[str, Any]:
        """Analyze target URL untuk vulnerabilities
        
        Args:
            target_url: URL target untuk dianalisis
            deep_scan: Melakukan deep scan jika True
            
        Returns:
            Dictionary berisi hasil analisis
        """
        logger.info(f"Starting analysis for target: {target_url}")
        
        results = {
            "target": target_url,
            "timestamp": datetime.now().isoformat(),
            "reconnaissance": {},
            "vulnerabilities": [],
            "ml_predictions": [],
            "risk_score": 0,
        }
        
        try:
            # Phase 1: Reconnaissance
            logger.info("Phase 1: Reconnaissance")
            results["reconnaissance"] = self.recon.gather_info(target_url)
            
            # Phase 2: Vulnerability Scanning
            logger.info("Phase 2: Vulnerability Scanning")
            results["vulnerabilities"] = self.scanner.scan(target_url, deep=deep_scan)
            
            # Phase 3: ML-based Prediction
            logger.info("Phase 3: ML Analysis")
            results["ml_predictions"] = self.ml_predictor.predict(results["vulnerabilities"])
            
            # Phase 4: Risk Analysis
            logger.info("Phase 4: Risk Analysis")
            results["risk_score"] = self.risk_analyzer.calculate_risk_score(
                results["vulnerabilities"]
            )
            
            logger.info(f"Analysis completed. Risk Score: {results['risk_score']}")
            
        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}")
            raise
        
        return results

    def analyze_code(self, code_path: str) -> Dict[str, Any]:
        """Analyze source code untuk security issues
        
        Args:
            code_path: Path ke source code
            
        Returns:
            Dictionary berisi code security analysis results
        """
        logger.info(f"Starting code analysis for: {code_path}")
        
        results = {
            "code_path": code_path,
            "timestamp": datetime.now().isoformat(),
            "issues": [],
            "severity_distribution": {},
        }
        
        try:
            results["issues"] = self.scanner.scan_code(code_path)
            results["severity_distribution"] = self._calculate_severity_distribution(
                results["issues"]
            )
        except Exception as e:
            logger.error(f"Error during code analysis: {str(e)}")
            raise
        
        return results

    def generate_report(self, analysis_results: Dict, format: str = "pdf") -> str:
        """Generate report dari hasil analisis
        
        Args:
            analysis_results: Hasil dari analyze_target atau analyze_code
            format: Format report (pdf, html, json)
            
        Returns:
            Path ke generated report
        """
        logger.info(f"Generating {format} report")
        return self.report_generator.generate(analysis_results, format=format)

    @staticmethod
    def _calculate_severity_distribution(issues: List[Dict]) -> Dict[str, int]:
        """Calculate severity distribution dari issues list"""
        distribution = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0,
        }
        
        for issue in issues:
            severity = issue.get("severity", "info").lower()
            if severity in distribution:
                distribution[severity] += 1
        
        return distribution
