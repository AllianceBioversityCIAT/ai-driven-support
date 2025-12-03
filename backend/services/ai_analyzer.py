"""
AI Ticket Analyzer Service
Analyzes support tickets using OpenAI to provide:
- Summary
- Possible category
- Possible automations
- User sentiment/feelings
"""
import logging
from typing import Optional, Dict, Any
import json
from openai import OpenAI
import os

logger = logging.getLogger(__name__)


class TicketAnalyzer:
    """Analyzes tickets using OpenAI API"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ticket analyzer
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OpenAI API key not configured")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

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
                "message": "OpenAI API key not configured",
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

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt(),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1000,
                response_format={"type": "json_object"},
            )

            # Parse response
            response_text = response.choices[0].message.content
            analysis_result = json.loads(response_text)

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
        return """You are a professional support ticket analyzer. Your role is to analyze support tickets and provide structured insights WITHOUT hallucinating or making assumptions beyond what is explicitly stated in the ticket.

IMPORTANT RULES:
1. Only analyze what is explicitly written in the ticket
2. Do NOT invent information or make assumptions about missing data
3. Do NOT categorize based on assumptions - suggest categories based ONLY on what's mentioned
4. Provide factual analysis based solely on the ticket content
5. Be conservative in your assessments

Respond with a JSON object containing your analysis."""

    def _create_analysis_prompt(self, subject: str, description: str) -> str:
        """Create the analysis prompt"""
        return f"""Analyze the following support ticket and provide insights in JSON format.

TICKET SUBJECT: {subject}

TICKET DESCRIPTION:
{description}

Provide a JSON response with the following structure (ONLY include these fields):
{{
    "summary": "A concise 2-3 sentence summary of the ticket issue (based ONLY on what's stated)",
    "possible_categories": [
        {{
            "category": "Category name",
            "confidence": "high/medium/low",
            "reason": "Why this category based on ticket content"
        }}
    ],
    "possible_automations": [
        {{
            "automation": "What could be automated",
            "description": "How it would work",
            "feasibility": "high/medium/low"
        }}
    ],
    "user_sentiment": {{
        "overall_feeling": "positive/neutral/negative/frustrated/urgent",
        "indicators": ["List of text indicators that suggest this feeling"],
        "urgency_level": "low/medium/high/critical"
    }}
}}

IMPORTANT:
- summary: Extract only what's explicitly mentioned, don't infer additional problems
- possible_categories: Only suggest categories that are clearly hinted at or mentioned in the ticket
- possible_automations: Suggest automations that would directly solve or help with the stated issue
- user_sentiment: Analyze tone and language - look for keywords indicating emotion, frustration, politeness, etc.
- confidence/feasibility: Be conservative - use "low" if not clear"""

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
