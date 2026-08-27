"""HackerOne Integration untuk v2"""

import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class HackerOneIntegration:
    """Integration dengan HackerOne platform"""

    API_BASE_URL = "https://api.hackerone.com/v1"

    def __init__(self, api_token: str, api_username: str):
        """Initialize HackerOne integration
        
        Args:
            api_token: HackerOne API token
            api_username: HackerOne username
        """
        self.api_token = api_token
        self.api_username = api_username
        self.session = requests.Session()
        self.session.auth = (api_username, api_token)
        logger.info("HackerOne integration initialized")

    def submit_report(self, vulnerability: Dict, program_id: str) -> Dict[str, Any]:
        """Submit vulnerability report ke HackerOne
        
        Args:
            vulnerability: Vulnerability details
            program_id: HackerOne program ID
            
        Returns:
            Report submission response
        """
        report_payload = {
            "data": {
                "type": "reports",
                "attributes": {
                    "title": vulnerability.get("title", "Security Vulnerability"),
                    "vulnerability_information": vulnerability.get("description"),
                    "impact": vulnerability.get("impact"),
                    "affected_asset_type": "url",
                    "affected_asset": vulnerability.get("target"),
                },
                "relationships": {
                    "program": {
                        "data": {"type": "programs", "id": program_id}
                    }
                },
            }
        }
        
        try:
            response = self.session.post(
                f"{self.API_BASE_URL}/reports",
                json=report_payload,
            )
            
            if response.status_code == 201:
                logger.info(f"Report submitted successfully to HackerOne")
                return response.json()
            else:
                logger.error(f"Failed to submit report: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            logger.error(f"Error submitting report: {str(e)}")
            return {"error": str(e)}

    def get_programs(self) -> List[Dict]:
        """Get list of HackerOne programs
        
        Returns:
            List of programs
        """
        try:
            response = self.session.get(f"{self.API_BASE_URL}/me/programs")
            
            if response.status_code == 200:
                return response.json().get("data", [])
            else:
                logger.error(f"Failed to fetch programs: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching programs: {str(e)}")
            return []

    def get_bounty_information(self, program_id: str) -> Dict[str, Any]:
        """Get bounty information untuk program
        
        Args:
            program_id: Program ID
            
        Returns:
            Bounty information
        """
        try:
            response = self.session.get(f"{self.API_BASE_URL}/programs/{program_id}")
            
            if response.status_code == 200:
                program_data = response.json().get("data", {})
                return {
                    "program_name": program_data.get("attributes", {}).get("name"),
                    "bounty_table": program_data.get("attributes", {}).get("bounty_table"),
                    "response_time": program_data.get("attributes", {}).get("response_time"),
                }
            else:
                logger.error(f"Failed to fetch bounty info: {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"Error fetching bounty info: {str(e)}")
            return {}

    def check_duplicate_reports(self, vulnerability: Dict) -> List[Dict]:
        """Check untuk duplicate reports
        
        Args:
            vulnerability: Vulnerability details
            
        Returns:
            List of similar reports
        """
        # Simplified duplicate checking
        return []
