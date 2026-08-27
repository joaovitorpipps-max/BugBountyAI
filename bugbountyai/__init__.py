"""Main BugBountyAI module dengan Gemini AI integration"""

from bugbountyai.core.analyzer import BugBountyAnalyzer
from bugbountyai.ai.gemini_analyzer import GeminiAIAnalyzer
from bugbountyai.ai.gemini_report_generator import GeminiAIReportGenerator
from bugbountyai.exploitation.auto_exploit import AutoExploitationEngine
from bugbountyai.monitoring.realtime_monitor import RealtimeMonitor
from bugbountyai.integrations.hackerone_integration import HackerOneIntegration
from bugbountyai.integrations.bugcrowd_integration import BugcrowdIntegration
from bugbountyai.enterprise.multi_user_system import MultiUserSystem
from bugbountyai.scanning.advanced_scanner import AdvancedScanner
from bugbountyai.fuzzing.intelligent_fuzzer import IntelligentFuzzer
from bugbountyai.reporting.professional_reports import ProfessionalReportGenerator
from bugbountyai.audit.audit_logger import AuditLogger

__version__ = "2.0.0"
__author__ = "BugBountyAI Team"
__description__ = "AI-Powered Bug Bounty Security Vulnerability Scanner with Gemini AI Integration"

__all__ = [
    "BugBountyAnalyzer",
    "GeminiAIAnalyzer",
    "GeminiAIReportGenerator",
    "AutoExploitationEngine",
    "RealtimeMonitor",
    "HackerOneIntegration",
    "BugcrowdIntegration",
    "MultiUserSystem",
    "AdvancedScanner",
    "IntelligentFuzzer",
    "ProfessionalReportGenerator",
    "AuditLogger",
]

print("""
╔══════════════════════════════════════════════════════════════╗
║           BugBountyAI v2 + Gemini AI Integration                 ║
║    AI-Powered Bug Bounty Security Vulnerability Scanner        ║
╚══════════════════════════════════════════════════════════════╝
""")
