"""Gemini AI Integration untuk BugBountyAI v2"""

import logging
import google.generativeai as genai
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class GeminiAIAnalyzer:
    """Integration dengan Google Gemini AI untuk advanced analysis"""

    def __init__(self, api_key: str):
        """Initialize Gemini AI analyzer
        
        Args:
            api_key: Google Gemini API Key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        logger.info("Gemini AI Analyzer initialized")

    def analyze_vulnerability_with_gemini(self, vulnerability: Dict) -> Dict[str, Any]:
        """Analyze vulnerability menggunakan Gemini AI untuk insights mendalam
        
        Args:
            vulnerability: Vulnerability details
            
        Returns:
            Enhanced analysis dengan Gemini insights
        """
        prompt = f"""
Analisislah vulnerability berikut secara mendalam dan berikan insights keamanan:

Tipe: {vulnerability.get('type', 'Unknown')}
Deskripsi: {vulnerability.get('description', 'N/A')}
Endpoint: {vulnerability.get('endpoint', 'N/A')}
Severity: {vulnerability.get('severity', 'Unknown')}
Confidence: {vulnerability.get('confidence', 0)}

Berikan:
1. Root cause analysis
2. Potential impact
3. Attack vectors
4. Recommended fixes
5. Risk assessment
"""
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            return {
                "vulnerability_type": vulnerability.get('type'),
                "gemini_analysis": analysis_text,
                "timestamp": datetime.now().isoformat(),
                "model": "Gemini Pro",
            }
        except Exception as e:
            logger.error(f"Error analyzing vulnerability with Gemini: {str(e)}")
            return {"error": str(e)}

    def generate_exploitation_strategy(self, vulnerability: Dict, target: str) -> Dict[str, Any]:
        """Generate smart exploitation strategy menggunakan Gemini AI
        
        Args:
            vulnerability: Vulnerability details
            target: Target URL
            
        Returns:
            Exploitation strategy powered by Gemini
        """
        prompt = f"""
Buatkan strategi eksploitasi untuk vulnerability berikut:

Target: {target}
Vulnerability Type: {vulnerability.get('type')}
Description: {vulnerability.get('description')}
Endpoint: {vulnerability.get('endpoint')}

Berikan:
1. Step-by-step exploitation process
2. Required tools
3. Expected outcomes
4. Detection evasion techniques
5. Post-exploitation actions

Format: Detailed technical guide
"""
        
        try:
            response = self.model.generate_content(prompt)
            strategy = response.text
            
            return {
                "target": target,
                "vulnerability": vulnerability.get('type'),
                "exploitation_strategy": strategy,
                "generated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error generating exploitation strategy: {str(e)}")
            return {"error": str(e)}

    def generate_fix_recommendations(self, vulnerability: Dict, tech_stack: List[str]) -> Dict[str, Any]:
        """Generate smart fix recommendations dari Gemini AI
        
        Args:
            vulnerability: Vulnerability details
            tech_stack: Technology stack used
            
        Returns:
            Fix recommendations dengan code examples
        """
        prompt = f"""
Buatkan rekomendasi fix untuk vulnerability berikut:

Tipe Vulnerability: {vulnerability.get('type')}
Deskripsi: {vulnerability.get('description')}
Tech Stack: {', '.join(tech_stack)}

Berikan:
1. Root cause explanation
2. Step-by-step fix guide
3. Code examples untuk {tech_stack[0] if tech_stack else 'general'}
4. Best practices untuk prevent
5. Testing procedures
6. Security checklist

Format: Developer-friendly dengan code snippets
"""
        
        try:
            response = self.model.generate_content(prompt)
            recommendations = response.text
            
            return {
                "vulnerability": vulnerability.get('type'),
                "recommendations": recommendations,
                "tech_stack": tech_stack,
                "generated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error generating fix recommendations: {str(e)}")
            return {"error": str(e)}

    def analyze_target_security_posture(self, target: str, scan_results: Dict) -> Dict[str, Any]:
        """Analyze overall security posture menggunakan Gemini AI
        
        Args:
            target: Target URL
            scan_results: Complete scan results
            
        Returns:
            Comprehensive security assessment
        """
        vulnerabilities_summary = f"""
Vulnerabilities found: {len(scan_results.get('vulnerabilities', []))}
Risk Score: {scan_results.get('risk_score', 0)}/100
Severity Distribution:
  Critical: {len([v for v in scan_results.get('vulnerabilities', []) if v.get('severity') == 'critical'])}
  High: {len([v for v in scan_results.get('vulnerabilities', []) if v.get('severity') == 'high'])}
  Medium: {len([v for v in scan_results.get('vulnerabilities', []) if v.get('severity') == 'medium'])}
  Low: {len([v for v in scan_results.get('vulnerabilities', []) if v.get('severity') == 'low'])}
"""
        
        prompt = f"""
Analisis postur keamanan keseluruhan untuk target berikut:

Target: {target}
{vulnerabilities_summary}

Berikan:
1. Overall security rating (A-F)
2. Key security concerns
3. Risk prioritization
4. Quick wins (easy fixes)
5. Long-term strategy
6. Industry benchmarking
7. Compliance readiness assessment

Format: Executive summary + detailed analysis
"""
        
        try:
            response = self.model.generate_content(prompt)
            assessment = response.text
            
            return {
                "target": target,
                "security_assessment": assessment,
                "scan_date": datetime.now().isoformat(),
                "model_used": "Gemini Pro",
            }
        except Exception as e:
            logger.error(f"Error analyzing security posture: {str(e)}")
            return {"error": str(e)}

    def generate_executive_summary(self, scan_results: Dict, target: str) -> str:
        """Generate executive summary powered by Gemini AI
        
        Args:
            scan_results: Complete scan results
            target: Target URL
            
        Returns:
            Executive summary text
        """
        vulnerabilities = scan_results.get('vulnerabilities', [])
        
        prompt = f"""
Buatkan executive summary untuk vulnerability scan report:

Target: {target}
Risk Score: {scan_results.get('risk_score', 0)}/100
Total Vulnerabilities: {len(vulnerabilities)}

Top Vulnerabilities:
{chr(10).join([f"- {v.get('type')} ({v.get('severity')})" for v in vulnerabilities[:5]])}

Buat:
1. Professional executive summary (2-3 paragraphs)
2. Key findings highlights
3. Business impact assessment
4. Immediate action items
5. Success metrics

Format: C-level executive friendly, non-technical
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            return ""

    def analyze_code_security(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze source code security menggunakan Gemini AI
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Code security analysis
        """
        prompt = f"""
Analisis keamanan source code berikut ({language}):

```{language}
{code[:2000]}  # Limit to 2000 chars
```

Identifikasi:
1. Security vulnerabilities
2. Bad practices
3. Potential exploits
4. OWASP Top 10 issues
5. Recommended fixes
6. Code improvement suggestions

Format: Developer-friendly security review
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                "language": language,
                "code_analysis": response.text,
                "analyzed_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error analyzing code security: {str(e)}")
            return {"error": str(e)}

    def predict_zero_day_patterns(self, target_info: Dict, tech_stack: List[str]) -> Dict[str, Any]:
        """Predict potential zero-day patterns menggunakan Gemini AI
        
        Args:
            target_info: Target information
            tech_stack: Technologies used
            
        Returns:
            Zero-day pattern predictions
        """
        prompt = f"""
Prediksi potential zero-day atau advanced vulnerabilities untuk target berikut:

Target: {target_info.get('url', 'Unknown')}
Tech Stack: {', '.join(tech_stack)}
Framework: {target_info.get('framework', 'Unknown')}
Database: {target_info.get('database', 'Unknown')}

Berikan:
1. Potential zero-day vectors
2. Advanced exploitation techniques
3. Supply chain risks
4. Dependency vulnerabilities
5. API abuse patterns
6. Architectural weaknesses
7. Mitigation strategies

Format: Technical threat assessment
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            return {
                "target": target_info.get('url'),
                "predictions": response.text,
                "confidence": "High",
                "generated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            logger.error(f"Error predicting zero-day patterns: {str(e)}")
            return {"error": str(e)}
