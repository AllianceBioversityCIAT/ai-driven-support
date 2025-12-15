"""
AI Ticket Analyzer Service
Legacy service - delegates to infrastructure layer
Use infrastructure.ai_providers.BedrockAIProvider for new code
"""
import logging
from typing import Optional, Dict, Any
import re
from infrastructure.ai_providers import BedrockAIProvider
from prompts import TICKET_ANALYSIS_SYSTEM_PROMPT, TICKET_ANALYSIS_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


def clean_html(html_text: str) -> str:
    """Remove HTML tags and decode entities from text"""
    if not html_text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', html_text)
    
    # Decode common HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


class TicketAnalyzer:
    """Analyzes tickets using AWS Bedrock API - Legacy adapter"""

    def __init__(self, aws_access_key: Optional[str] = None, aws_secret_key: Optional[str] = None):
        """
        Initialize the ticket analyzer

        Args:
            aws_access_key: AWS Access Key (defaults to AWS_ACCESS_KEY env var)
            aws_secret_key: AWS Secret Key (defaults to AWS_SECRET_ACCESS_KEY env var)
        """
        self.provider = BedrockAIProvider(aws_access_key, aws_secret_key)
        self.client = self.provider.client

    def analyze_ticket(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a ticket and provide insights

        Args:
            ticket_data: Dictionary containing ticket information

        Returns:
            Dictionary with analysis results or error
        """
        if not self.client:
            return {
                "status": "error",
                "message": "AWS credentials not configured",
                "ticket_id": ticket_data.get("id"),
            }

        try:
            # Log incoming ticket data for debugging
            logger.info(f"[AI] Received ticket_data keys: {list(ticket_data.keys()) if ticket_data else 'None'}")
            
            ticket_id = ticket_data.get("id")
            subject = ticket_data.get("subject", "")
            description = ticket_data.get("description", "")
            description_text = ticket_data.get("description_text", "")

            # Clean HTML from descriptions
            if description and not description_text:
                description = clean_html(description)
            
            # Use description_text if available, otherwise use cleaned description
            full_description = description_text or description
            
            logger.info(f"[AI] Analyzing ticket {ticket_id}...")
            logger.info(f"[AI] Subject: {subject[:50] if subject else 'EMPTY'}...")
            logger.info(f"[AI] Description length: {len(full_description)}")
            logger.info(f"[AI] Description preview: {full_description[:100] if full_description else 'EMPTY'}...")

            if not subject and not full_description:
                logger.warning(f"[AI] Empty ticket data received for ticket {ticket_id}")
                return {
                    "status": "error",
                    "message": "Ticket has no subject or description to analyze",
                    "ticket_id": ticket_id,
                }

            prompt = self._create_analysis_prompt(subject, full_description)
            system_prompt = self._get_system_prompt()
            
            analysis_result = self.provider.analyze(system_prompt, prompt)

            logger.info(f"[AI] Analysis complete for ticket {ticket_id}")

            return {
                "status": "success",
                "ticket_id": ticket_id,
                "analysis": analysis_result,
            }

        except Exception as e:
            logger.error(f"[AI] Error analyzing ticket: {str(e)}")
            return {
                "status": "error",
                "message": f"Analysis failed: {str(e)}",
                "ticket_id": ticket_data.get("id"),
            }

    def _get_system_prompt(self) -> str:
        """Get the system prompt for consistent AI behavior"""
        return TICKET_ANALYSIS_SYSTEM_PROMPT

    def _create_analysis_prompt(self, subject: str, description: str) -> str:
        """Create the analysis prompt"""
        return TICKET_ANALYSIS_PROMPT_TEMPLATE.format(
            subject=subject,
            description=description
        )

    def analyze_multiple_tickets(
        self, tickets: list
    ) -> Dict[str, Any]:
        """
        Analyze multiple tickets

        Args:
            tickets: List of ticket dictionaries

        Returns:
            Dictionary with batch analysis results
        """
        results = []
        failed = []

        for ticket in tickets:
            result = self.analyze_ticket(ticket)
            if result["status"] == "success":
                results.append(result)
            else:
                failed.append(result)

        return {
            "status": "batch_analysis_complete",
            "total": len(tickets),
            "successful": len(results),
            "failed": len(failed),
            "results": results,
            "failures": failed,
        }
