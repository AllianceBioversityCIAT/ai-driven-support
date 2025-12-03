"""
AI Ticket Analyzer Service
Analyzes support tickets using AWS Bedrock to provide:
- Summary
- Possible category
- Possible automations
- User sentiment/feelings
"""
import logging
from typing import Optional, Dict, Any
import json
import boto3
import os
import re
from prompts import TICKET_ANALYSIS_SYSTEM_PROMPT, TICKET_ANALYSIS_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


class TicketAnalyzer:
    """Analyzes tickets using AWS Bedrock API"""

    def __init__(self, aws_access_key: Optional[str] = None, aws_secret_key: Optional[str] = None):
        """
        Initialize the ticket analyzer

        Args:
            aws_access_key: AWS Access Key (defaults to AWS_ACCESS_KEY env var)
            aws_secret_key: AWS Secret Key (defaults to AWS_SECRET_ACCESS_KEY env var)
        """
        self.aws_access_key = aws_access_key or os.getenv("AWS_ACCESS_KEY")
        self.aws_secret_key = aws_secret_key or os.getenv("AWS_SECRET_ACCESS_KEY")

        if not self.aws_access_key or not self.aws_secret_key:
            logger.warning("AWS credentials not configured")
            self.client = None
        else:
            try:
                self.client = boto3.client(
                    'bedrock-runtime',
                    region_name='us-east-1',
                    aws_access_key_id=self.aws_access_key,
                    aws_secret_access_key=self.aws_secret_key
                )
                logger.info("[AI] AWS Bedrock client initialized")
            except Exception as e:
                logger.error(f"[AI] Failed to initialize AWS Bedrock: {str(e)}")
                self.client = None

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
            # Extract ticket information
            ticket_id = ticket_data.get("id")
            subject = ticket_data.get("subject", "")
            description = ticket_data.get("description", "")
            description_text = ticket_data.get("description_text", "")

            # Use description_text if available, otherwise use description
            full_description = description_text or description

            logger.info(f"[AI] Analyzing ticket {ticket_id}...")

            # Create the analysis prompt
            prompt = self._create_analysis_prompt(subject, full_description)

            # Call AWS Bedrock API with Claude 3.5 Sonnet
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "system": self._get_system_prompt(),
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            response = self.client.invoke_model(
                modelId="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                body=json.dumps(body)
            )

            # Parse Bedrock response
            response_body = json.loads(response['body'].read())

            # Debug: log the response structure
            logger.info(f"[AI] Response structure: {response_body}")

            response_text = response_body.get('content', [{}])[0].get('text', '').strip()
            if not response_text:
                logger.error(f"[AI] Empty response text. Full response: {response_body}")
                raise ValueError("Empty response text from Bedrock model")

            logger.info(f"[AI] Response text: {response_text[:200]}")
            
            # Extract JSON from markdown code blocks if present
            import re
            json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                logger.info(f"[AI] Extracted JSON from markdown: {json_str[:100]}")
            else:
                json_str = response_text
                logger.info(f"[AI] Using raw response text as JSON")
            
            analysis_result = json.loads(json_str)

            logger.info(f"[AI] Analysis complete for ticket {ticket_id}")

            return {
                "status": "success",
                "ticket_id": ticket_id,
                "analysis": analysis_result,
            }

        except json.JSONDecodeError as e:
            logger.error(f"[AI] JSON parsing error: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to parse AI response: {str(e)}",
                "ticket_id": ticket_data.get("id"),
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
