"""Enhanced CLI dengan Gemini AI Integration"""

import click
import logging
from bugbountyai.core.analyzer import BugBountyAnalyzer
from bugbountyai.ai.gemini_analyzer import GeminiAIAnalyzer
from bugbountyai.ai.gemini_report_generator import GeminiAIReportGenerator
import os

logger = logging.getLogger(__name__)


@click.command()
@click.argument('target_url')
@click.option('--gemini-key', prompt='Gemini API Key', hide_input=True, help='Google Gemini API Key')
@click.option('--deep', is_flag=True, help='Perform deep scanning')
@click.option('--exploit', is_flag=True, help='Auto-exploit vulnerabilities')
@click.option('--ai-analysis', is_flag=True, default=True, help='Enable Gemini AI analysis')
@click.option('--report', type=click.Choice(['pdf', 'html', 'json']), default='pdf', help='Report format')
@click.option('--output', type=click.Path(), help='Output file path')
def scan_with_gemini(target_url: str, gemini_key: str, deep: bool, exploit: bool, ai_analysis: bool, report: str, output: str):
    """🔍 Scan target URL dengan Gemini AI powered analysis
    
    Example:
        bugbountyai scan-gemini https://target.com --gemini-key YOUR_KEY
        bugbountyai scan-gemini https://target.com --gemini-key YOUR_KEY --deep --exploit
    """
    click.echo(f"\n{'='*70}")
    click.echo(f"🧠 BugBountyAI v2 + Gemini AI - Security Scanner")
    click.echo(f"{'='*70}")
    click.echo(f"🎯 Target: {target_url}")
    click.echo(f"🧠 Gemini AI Analysis: {'Enabled' if ai_analysis else 'Disabled'}")
    click.echo(f"⚙️  Deep Scan: {'Yes' if deep else 'No'}")
    click.echo(f"💣 Auto Exploit: {'Yes' if exploit else 'No'}")
    click.echo(f"{'='*70}\n")
    
    try:
        # Validate Gemini API Key
        if not gemini_key:
            click.secho("❌ Gemini API Key is required!", fg='red', bold=True)
            raise click.Abort()
        
        # Initialize analyzer
        analyzer = BugBountyAnalyzer(api_key="default")
        gemini_analyzer = GeminiAIAnalyzer(api_key=gemini_key) if ai_analysis else None
        
        # Show progress
        with click.progressbar(
            length=100,
            label='Scanning with Gemini AI',
            show_pos=True
        ) as bar:
            # Phase 1: Reconnaissance
            click.echo("\n📡 Phase 1: Reconnaissance...")
            bar.update(15)
            
            # Phase 2: Vulnerability Scanning
            click.echo("🔎 Phase 2: Vulnerability Scanning...")
            results = analyzer.analyze_target(target_url, deep_scan=deep)
            bar.update(20)
            
            # Phase 3: Gemini AI Analysis
            if ai_analysis and gemini_analyzer:
                click.echo("🧠 Phase 3: Gemini AI Analysis...")
                
                # Analyze each vulnerability with Gemini
                for i, vuln in enumerate(results.get('vulnerabilities', [])):
                    gemini_analysis = gemini_analyzer.analyze_vulnerability_with_gemini(vuln)
                    vuln['ai_analysis'] = gemini_analysis.get('gemini_analysis', '')
                    
                    # Get fix recommendations
                    fix_recs = gemini_analyzer.generate_fix_recommendations(
                        vuln,
                        results.get('tech_stack', [])
                    )
                    vuln['fix_recommendations'] = fix_recs.get('recommendations', '')
                    
                    bar.update(int(40 / len(results.get('vulnerabilities', []))))
            else:
                bar.update(40)
            
            # Phase 4: Auto Exploitation
            if exploit and results['vulnerabilities']:
                click.echo("💣 Phase 4: Auto Exploitation...")
                from bugbountyai.exploitation.auto_exploit import AutoExploitationEngine
                exploit_engine = AutoExploitationEngine()
                exploit_results = exploit_engine.auto_exploit(
                    target_url,
                    results['vulnerabilities']
                )
                results['exploitations'] = exploit_results
                bar.update(15)
            else:
                bar.update(15)
            
            # Phase 5: Report Generation
            click.echo("📄 Phase 5: Report Generation...")
            bar.update(10)
        
        # Display results
        click.echo(f"\n{'='*70}")
        click.echo("📊 SCAN RESULTS - POWERED BY GEMINI AI")
        click.echo(f"{'='*70}")
        click.echo(f"🎯 Target: {results['target']}")
        click.echo(f"📅 Timestamp: {results['timestamp']}")
        click.echo(f"🚨 Risk Score: {results['risk_score']}/100")
        click.echo(f"🔴 Vulnerabilities Found: {len(results['vulnerabilities'])}")
        
        # Show vulnerability summary
        if results['vulnerabilities']:
            click.echo(f"\n{'─'*70}")
            click.echo("Vulnerabilities:")
            click.echo(f"{'─'*70}")
            
            severity_colors = {
                'critical': click.style('CRITICAL', fg='red', bold=True),
                'high': click.style('HIGH', fg='red'),
                'medium': click.style('MEDIUM', fg='yellow'),
                'low': click.style('LOW', fg='blue'),
                'info': click.style('INFO', fg='cyan'),
            }
            
            for i, vuln in enumerate(results['vulnerabilities'][:5], 1):
                severity = vuln.get('severity', 'unknown').lower()
                color_severity = severity_colors.get(severity, severity)
                click.echo(f"  {i}. [{color_severity}] {vuln.get('type', 'Unknown')}")
                click.echo(f"     Description: {vuln.get('description', 'N/A')}")
                
                # Show Gemini AI analysis if available
                if 'ai_analysis' in vuln:
                    click.echo(f"     🧠 Gemini AI Analysis:")
                    ai_text = vuln['ai_analysis'][:200] + "..." if len(vuln['ai_analysis']) > 200 else vuln['ai_analysis']
                    click.echo(f"     {ai_text}")
        
        # Generate report
        click.echo(f"\n{'─'*70}")
        click.echo("📄 Generating Report...")
        
        if ai_analysis and gemini_analyzer:
            # Generate Gemini AI powered report
            report_generator = GeminiAIReportGenerator(gemini_key=gemini_key)
            
            if report == 'pdf':
                report_path = report_generator.generate_pdf_report(
                    results,
                    target_url,
                    output or f"bugbountyai_report_{target_url.split('//')[1]}.pdf"
                )
            elif report == 'json':
                report_path = report_generator.generate_json_report(
                    results,
                    target_url,
                    output or f"bugbountyai_report_{target_url.split('//')[1]}.json"
                )
            else:
                # Default to text
                report_content = report_generator.generate_comprehensive_report(results, target_url)
                report_path = output or f"bugbountyai_report_{target_url.split('//')[1]}.txt"
                with open(report_path, 'w') as f:
                    f.write(report_content)
        else:
            report_path = analyzer.generate_report(results, format=report)
        
        if output:
            import shutil
            shutil.copy(report_path, output)
            click.echo(f"✅ Report saved to: {click.style(output, fg='green', bold=True)}")
        else:
            click.echo(f"✅ Report saved to: {click.style(report_path, fg='green', bold=True)}")
        
        click.echo(f"{'='*70}\n")
        click.secho("🤖 Scan completed with Gemini AI analysis!", fg='green', bold=True)
        
    except Exception as e:
        click.secho(f"\n❌ Error: {str(e)}", fg='red', bold=True)
        logger.exception("Scan failed")
        raise click.Abort()
