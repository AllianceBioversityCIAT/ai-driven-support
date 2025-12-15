"""
Slack Notification Service
Sends notifications to Slack using webhooks
"""
import logging
import requests
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SlackNotificationService:
    """Service for sending notifications to Slack"""
    
    def __init__(self, webhook_url: str):
        """
        Initialize Slack notification service
        
        Args:
            webhook_url: Slack webhook URL
        """
        self.webhook_url = webhook_url
        logger.info("[SLACK] Slack notification service initialized")
    
    def send_ticket_analysis(self, ticket_id: str, analysis: Dict[str, Any], domain: str = "alliance") -> bool:
        """
        Send ticket analysis to Slack
        
        Args:
            ticket_id: Ticket ID
            analysis: Analysis result dictionary
            domain: FreshService domain (default: alliance)
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Extract analysis data
            summary = analysis.get("summary", "No summary available")
            categories = analysis.get("possible_categories", [])
            automations = analysis.get("possible_automations", [])
            sentiment = analysis.get("user_sentiment", {})
            
            # Build Slack message
            message = self._build_analysis_message(ticket_id, summary, categories, automations, sentiment, domain)
            
            # Send to Slack
            response = requests.post(
                self.webhook_url,
                json={"text": message},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"[SLACK] ✅ Analysis sent to Slack for ticket {ticket_id}")
                return True
            else:
                logger.error(f"[SLACK] ❌ Failed to send to Slack: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"[SLACK] ❌ Error sending to Slack: {str(e)}")
            return False
    
    def _build_analysis_message(
        self, 
        ticket_id: str, 
        summary: str, 
        categories: list, 
        automations: list,
        sentiment: dict,
        domain: str = "alliance"
    ) -> str:
        """Build formatted Slack message"""
        
        # Ticket URL
        ticket_url = f"https://{domain}.freshservice.com/a/tickets/{ticket_id}?current_tab=details"
        
        # Header with clickable link
        message = f"🎫 *<{ticket_url}|Ticket #{ticket_id}>*\n\n"
        
        # Summary
        message += f"📝 *Summary:*\n{summary}\n\n"
        
        # Sentiment
        if sentiment:
            feeling = sentiment.get("overall_feeling", "unknown")
            urgency = sentiment.get("urgency_level", "unknown")
            
            feeling_emoji = {
                "positive": "😊",
                "neutral": "😐",
                "negative": "😞",
                "frustrated": "😤",
                "urgent": "🚨"
            }.get(feeling, "❓")
            
            urgency_emoji = {
                "low": "🟢",
                "medium": "🟡",
                "high": "🟠",
                "critical": "🔴"
            }.get(urgency, "⚪")
            
            message += f"💭 *Sentiment:* {feeling_emoji} {feeling.title()} | {urgency_emoji} Urgency: {urgency.upper()}\n\n"
        
        # Categories
        if categories:
            message += "🏷️ *Suggested Categories:*\n"
            for cat in categories[:3]:  # Top 3
                category = cat.get("category", "Unknown")
                confidence = cat.get("confidence", "low")
                confidence_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(confidence, "⚪")
                message += f"  • {confidence_emoji} {category} ({confidence} confidence)\n"
            message += "\n"
        
        # Automations
        if automations:
            message += "🤖 *Automation Opportunities:*\n"
            for auto in automations[:3]:  # Top 3
                automation = auto.get("automation", "Unknown")
                feasibility = auto.get("feasibility", "low")
                feasibility_emoji = {"high": "✅", "medium": "⚡", "low": "💡"}.get(feasibility, "❓")
                message += f"  • {feasibility_emoji} {automation}\n"
            message += "\n"
        
        # Footer
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message += f"⏰ _Analyzed at {timestamp}_"
        
        return message
    
    def send_simple_message(self, message: str) -> bool:
        """
        Send a simple text message to Slack
        
        Args:
            message: Message text
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            response = requests.post(
                self.webhook_url,
                json={"text": message},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info("[SLACK] ✅ Message sent to Slack")
                return True
            else:
                logger.error(f"[SLACK] ❌ Failed to send message: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"[SLACK] ❌ Error sending message: {str(e)}")
            return False
