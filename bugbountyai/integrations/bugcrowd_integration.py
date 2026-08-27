"""Bugcrowd Integration untuk v2"""

import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class BugcrowdIntegration:
    """Integration dengan Bugcrowd platform"""

    API_BASE_URL = "https://api.bugcrowd.com/v4"

    def __init__(self, api_token: str):
        """Initialize Bugcrowd integration
        
        Args:
            api_token: Bugcrowd API token
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Token {api_token}"})
        logger.info("Bugcrowd integration initialized")

    def submit_submission(self, vulnerability: Dict, program_id: str) -> Dict[str, Any]:
        """Submit vulnerability ke Bugcrowd
        
        Args:
            vulnerability: Vulnerability details
            program_id: Bugcrowd program ID
            
        Returns:
            Submission response
        """
        submission_payload = {
            "vulnerability_report": {
                "title": vulnerability.get("title", "Security Vulnerability"),
                "description": vulnerability.get("description"),
                "cvss_score": vulnerability.get("cvss_score"),
                "vulnerable_assets": [vulnerability.get("target")],
                "proof_of_concept": vulnerability.get("poc"),
            }
        }
        
        try:
            response = self.session.post(
                f"{self.API_BASE_URL}/programs/{program_id}/submissions",
                json=submission_payload,
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"Submission sent to Bugcrowd")
                return response.json()
            else:
                logger.error(f"Failed to submit: {response.text}")
                return {"error": response.text}
                
        except Exception as e:
            logger.error(f"Error submitting to Bugcrowd: {str(e)}")
            return {"error": str(e)}

    def get_programs(self) -> List[Dict]:
        """Get list of Bugcrowd programs
        
        Returns:
            List of programs
        """
        try:
            response = self.session.get(f"{self.API_BASE_URL}/programs")
            
            if response.status_code == 200:
                return response.json().get("programs", [])
            else:
                logger.error(f"Failed to fetch programs: {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching programs: {str(e)}")
            return []

    def get_bounty_data(self, program_id: str) -> Dict[str, Any]:
        """Get bounty data untuk program
        
        Args:
            program_id: Program ID
            
        Returns:
            Bounty information
        """
        try:
            response = self.session.get(f"{self.API_BASE_URL}/programs/{program_id}")
            
            if response.status_code == 200:
                program_data = response.json().get("program", {})
                return {
                    "program_name": program_data.get("name"),
                    "scope": program_data.get("scope"),
                    "bounty_amounts": program_data.get("bounty_amounts"),
                }
            else:
                logger.error(f"Failed to fetch bounty data: {response.text}")
                return {}
                
        except Exception as e:
            logger.error(f"Error fetching bounty data: {str(e)}")
            return {}
