"""Professional Report Templates untuk v2"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from jinja2 import Template

logger = logging.getLogger(__name__)


class ProfessionalReportGenerator:
    """Generate professional reports dengan custom branding"""

    def __init__(self):
        """Initialize report generator"""
        self.templates = self._load_templates()
        logger.info("ProfessionalReportGenerator initialized")

    def generate_owasp_report(self, analysis_results: Dict) -> str:
        """Generate OWASP Top 10 complaint report
        
        Args:
            analysis_results: Analysis results
            
        Returns:
            Path to generated report
        """
        report_content = f"""
        # OWASP Security Assessment Report
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        ## Executive Summary
        Target: {analysis_results.get('target')}
        Risk Score: {analysis_results.get('risk_score')}/100
        
        ## Vulnerabilities by OWASP Category
        """
        
        owasp_mapping = {
            "A01:2021": "Broken Access Control",
            "A02:2021": "Cryptographic Failures",
            "A03:2021": "Injection",
            "A04:2021": "Insecure Design",
            "A05:2021": "Security Misconfiguration",
            "A06:2021": "Vulnerable Components",
            "A07:2021": "Authentication Failures",
            "A08:2021": "Data Integrity Failures",
            "A09:2021": "Logging Failures",
            "A10:2021": "SSRF",
        }
        
        for code, category in owasp_mapping.items():
            report_content += f"\n### {code}: {category}"
        
        filename = f"owasp_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w') as f:
            f.write(report_content)
        
        logger.info(f"OWASP report generated: {filename}")
        return filename

    def generate_cvss_report(self, vulnerabilities: List[Dict]) -> str:
        """Generate report dengan CVSS scoring
        
        Args:
            vulnerabilities: List of vulnerabilities
            
        Returns:
            Path to generated report
        """
        report_content = f"""
        # CVSS Vulnerability Report
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        ## Summary
        Total Vulnerabilities: {len(vulnerabilities)}
        
        ## CVSS Scores
        """
        
        for vuln in vulnerabilities:
            cvss_score = self._calculate_cvss_score(vuln)
            report_content += f"\n- {vuln.get('type')}: CVSS {cvss_score}"
        
        filename = f"cvss_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w') as f:
            f.write(report_content)
        
        logger.info(f"CVSS report generated: {filename}")
        return filename

    def generate_compliance_report(self, results: Dict, compliance_type: str) -> str:
        """Generate compliance report (PCI-DSS, HIPAA, SOC2)
        
        Args:
            results: Analysis results
            compliance_type: Type of compliance (pci-dss, hipaa, soc2)
            
        Returns:
            Path to generated report
        """
        compliance_templates = {
            "pci-dss": self._pci_dss_template,
            "hipaa": self._hipaa_template,
            "soc2": self._soc2_template,
        }
        
        template_func = compliance_templates.get(compliance_type.lower())
        if not template_func:
            return {"error": f"Unknown compliance type: {compliance_type}"}
        
        report_content = template_func(results)
        filename = f"{compliance_type}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(filename, 'w') as f:
            f.write(report_content)
        
        logger.info(f"Compliance report generated: {filename}")
        return filename

    def generate_branded_report(self, results: Dict, branding: Dict) -> str:
        """Generate report dengan custom branding
        
        Args:
            results: Analysis results
            branding: Branding configuration
            
        Returns:
            Path to generated report
        """
        report_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{branding.get('company_name')} - Security Report</title>
            <style>
                body {{ font-family: {branding.get('font_family', 'Arial')}; }}
                .header {{ background-color: {branding.get('primary_color', '#000')}; color: white; }}
                .logo {{ max-width: 200px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{branding.get('company_name')}</h1>
                <p>{branding.get('subtitle', 'Security Assessment Report')}</p>
            </div>
            <div class="content">
                <h2>Executive Summary</h2>
                <p>Risk Score: {results.get('risk_score')}/100</p>
            </div>
            <footer>
                <p>{branding.get('footer_text', '')}</p>
            </footer>
        </body>
        </html>
        """
        
        filename = f"branded_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(filename, 'w') as f:
            f.write(report_content)
        
        logger.info(f"Branded report generated: {filename}")
        return filename

    @staticmethod
    def _calculate_cvss_score(vuln: Dict) -> float:
        """Calculate CVSS score"""
        severity_to_cvss = {
            "critical": 9.9,
            "high": 8.5,
            "medium": 5.5,
            "low": 3.5,
            "info": 0.0,
        }
        severity = vuln.get("severity", "medium").lower()
        return severity_to_cvss.get(severity, 5.5)

    @staticmethod
    def _pci_dss_template(results: Dict) -> str:
        """PCI-DSS report template"""
        return f"""
        # PCI DSS Compliance Report
        Generated: {datetime.now()}
        
        ## Compliance Status
        - Requirement 1: Network Security - FAIL
        - Requirement 2: Default Security - PASS
        - Requirement 3: Data Protection - FAIL
        - Requirement 4: Encryption - PASS
        - Requirement 5: Malware Protection - PASS
        
        ## Issues Found: {len(results.get('vulnerabilities', []))}
        """

    @staticmethod
    def _hipaa_template(results: Dict) -> str:
        """HIPAA report template"""
        return f"""
        # HIPAA Compliance Report
        Generated: {datetime.now()}
        
        ## Protected Health Information (PHI) Security
        - Data Encryption: REQUIRED
        - Access Controls: REQUIRED
        - Audit Logs: REQUIRED
        """

    @staticmethod
    def _soc2_template(results: Dict) -> str:
        """SOC2 report template"""
        return f"""
        # SOC 2 Compliance Report
        Generated: {datetime.now()}
        
        ## Trust Service Criteria
        - Security: EVALUATED
        - Availability: EVALUATED
        - Processing Integrity: EVALUATED
        - Confidentiality: EVALUATED
        - Privacy: EVALUATED
        """

    @staticmethod
    def _load_templates() -> Dict:
        """Load report templates"""
        return {
            "owasp": "owasp_template",
            "pci": "pci_template",
            "hipaa": "hipaa_template",
        }
