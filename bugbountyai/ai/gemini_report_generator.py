"""AI-Powered Report Generator menggunakan Gemini AI"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from bugbountyai.ai.gemini_analyzer import GeminiAIAnalyzer

logger = logging.getLogger(__name__)


class GeminiAIReportGenerator:
    """Generate professional reports powered by Gemini AI"""

    def __init__(self, gemini_api_key: str):
        """Initialize AI report generator
        
        Args:
            gemini_api_key: Google Gemini API Key
        """
        self.gemini = GeminiAIAnalyzer(api_key=gemini_api_key)
        logger.info("Gemini AI Report Generator initialized")

    def generate_comprehensive_report(self, scan_results: Dict, target: str) -> str:
        """Generate comprehensive report powered by Gemini AI
        
        Args:
            scan_results: Complete scan results
            target: Target URL
            
        Returns:
            Full report content
        """
        report = f"""
{'='*80}
SECURITY VULNERABILITY ASSESSMENT REPORT
Powered by BugBountyAI v2 + Gemini AI
{'='*80}

Target: {target}
Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Report Generated: {datetime.now().isoformat()}

{'-'*80}
EXECUTIVE SUMMARY
{'-'*80}

"""
        
        # Generate executive summary using Gemini
        executive_summary = self.gemini.generate_executive_summary(scan_results, target)
        report += f"{executive_summary}\n\n"
        
        # Risk Overview
        report += f"""
{'-'*80}
RISK OVERVIEW
{'-'*80}
Risk Score: {scan_results.get('risk_score', 0)}/100
Total Vulnerabilities: {len(scan_results.get('vulnerabilities', []))}
Critical: {len([v for v in scan_results.get('vulnerabilities', []) if v.get('severity') == 'critical'])}
High: {len([v for v in scan_results.get('vulnerabilities', []) if v.get('severity') == 'high'])}
Medium: {len([v for v in scan_results.get('vulnerabilities', []) if v.get('severity') == 'medium'])}
Low: {len([v for v in scan_results.get('vulnerabilities', []) if v.get('severity') == 'low'])}

"""
        
        # Detailed Findings
        report += f"""
{'-'*80}
DETAILED FINDINGS
{'-'*80}

"""
        
        for i, vuln in enumerate(scan_results.get('vulnerabilities', []), 1):
            report += f"""
{i}. {vuln.get('type', 'Unknown Vulnerability')}
   Severity: {vuln.get('severity', 'Unknown').upper()}
   Endpoint: {vuln.get('endpoint', 'N/A')}
   Description: {vuln.get('description', 'N/A')}
   Confidence: {vuln.get('confidence', 0)}%

"""
            
            # Get Gemini AI analysis for this vulnerability
            ai_analysis = self.gemini.analyze_vulnerability_with_gemini(vuln)
            if 'gemini_analysis' in ai_analysis:
                report += f"   AI Analysis:\n   {ai_analysis['gemini_analysis']}\n\n"
            
            # Get fix recommendations
            tech_stack = scan_results.get('tech_stack', [])
            recommendations = self.gemini.generate_fix_recommendations(vuln, tech_stack)
            if 'recommendations' in recommendations:
                report += f"   Recommendations:\n   {recommendations['recommendations']}\n\n"
        
        # Security Assessment
        report += f"""
{'-'*80}
SECURITY POSTURE ASSESSMENT
{'-'*80}

"""
        assessment = self.gemini.analyze_target_security_posture(target, scan_results)
        if 'security_assessment' in assessment:
            report += f"{assessment['security_assessment']}\n\n"
        
        # Zero-Day Predictions
        report += f"""
{'-'*80}
ZERO-DAY & ADVANCED THREAT ASSESSMENT
{'-'*80}

"""
        predictions = self.gemini.predict_zero_day_patterns(
            target_info={'url': target},
            tech_stack=scan_results.get('tech_stack', [])
        )
        if 'predictions' in predictions:
            report += f"{predictions['predictions']}\n\n"
        
        # Conclusion
        report += f"""
{'-'*80}
CONCLUSION & NEXT STEPS
{'-'*80}

This security assessment was conducted using advanced AI analysis powered by
Google Gemini AI integration with BugBountyAI v2.

Immediate Actions Required:
1. Address all CRITICAL severity vulnerabilities
2. Implement recommended fixes
3. Conduct security training
4. Implement monitoring

Long-term Strategy:
1. Establish secure development lifecycle (SDLC)
2. Implement automated security testing
3. Conduct regular security audits
4. Maintain vulnerability management program

{'-'*80}
Report End
{'='*80}
"""
        
        return report

    def generate_pdf_report(self, scan_results: Dict, target: str, output_path: str) -> str:
        """Generate PDF report powered by Gemini AI
        
        Args:
            scan_results: Complete scan results
            target: Target URL
            output_path: Path to save PDF
            
        Returns:
            Path to generated PDF
        """
        report_content = self.generate_comprehensive_report(scan_results, target)
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.units import inch
            from datetime import datetime
            
            # Create PDF
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor='#1f4788',
                spaceAfter=30,
                alignment=1  # Center
            )
            
            # Add content
            story.append(Paragraph("Security Vulnerability Assessment Report", title_style))
            story.append(Paragraph(f"Target: {target}", styles['Normal']))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Spacer(1, 0.3*inch))
            
            # Add report content
            for line in report_content.split('\n'):
                if line.strip():
                    story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
            
            doc.build(story)
            logger.info(f"PDF report generated: {output_path}")
            return output_path
            
        except ImportError:
            logger.warning("reportlab not installed, saving as text")
            with open(output_path.replace('.pdf', '.txt'), 'w') as f:
                f.write(report_content)
            return output_path.replace('.pdf', '.txt')

    def generate_json_report(self, scan_results: Dict, target: str, output_path: str) -> str:
        """Generate JSON report
        
        Args:
            scan_results: Complete scan results
            target: Target URL
            output_path: Path to save JSON
            
        Returns:
            Path to generated JSON
        """
        import json
        
        report_data = {
            "target": target,
            "generated_at": datetime.now().isoformat(),
            "scan_results": scan_results,
            "ai_powered": True,
            "ai_model": "Gemini Pro",
        }
        
        # Add AI-enhanced data for each vulnerability
        enhanced_vulnerabilities = []
        for vuln in scan_results.get('vulnerabilities', []):
            enhanced_vuln = vuln.copy()
            
            # Get AI analysis
            ai_analysis = self.gemini.analyze_vulnerability_with_gemini(vuln)
            if 'gemini_analysis' in ai_analysis:
                enhanced_vuln['ai_analysis'] = ai_analysis['gemini_analysis']
            
            enhanced_vulnerabilities.append(enhanced_vuln)
        
        report_data['vulnerabilities_with_ai'] = enhanced_vulnerabilities
        
        with open(output_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"JSON report generated: {output_path}")
        return output_path
