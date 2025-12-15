"""
Ticket Analysis API Endpoints
"""
import logging
from fastapi import APIRouter, HTTPException
from config import config
from api.freshservice_client import FreshServiceClient
from ..application.analyze_ticket import AnalyzeTicketUseCase
from services.ai_analyzer import TicketAnalyzer

logger = logging.getLogger(__name__)

router = APIRouter()


def get_fs_client() -> FreshServiceClient:
    """Get FreshService client"""
    if not config.FRESHSERVICE_API_KEY or not config.FRESHSERVICE_DOMAIN:
        raise HTTPException(
            status_code=500,
            detail="FreshService credentials not configured"
        )
    return FreshServiceClient(
        api_key=config.FRESHSERVICE_API_KEY,
        domain=config.FRESHSERVICE_DOMAIN
    )


@router.post("/{ticket_id}/analyze")
async def analyze_ticket(ticket_id: str):
    """Analyze a single ticket with AI"""
    logger.info(f"🤖 Analyzing ticket: {ticket_id}")
    try:
        client = get_fs_client()
        ticket = client.get_ticket(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        analyzer = TicketAnalyzer()
        use_case = AnalyzeTicketUseCase(analyzer)
        
        result = use_case.execute(ticket)
        
        # Send notification to Slack if configured
        if config.SLACK_WEBHOOK_URL:
            try:
                from infrastructure.notifications import SlackNotificationService
                slack_service = SlackNotificationService(config.SLACK_WEBHOOK_URL)
                
                if result.get("status") == "success" and result.get("analysis"):
                    slack_service.send_ticket_analysis(
                        ticket_id, 
                        result["analysis"],
                        domain=config.FRESHSERVICE_DOMAIN
                    )
                    logger.info(f"[ENDPOINT] 📨 Slack notification sent for ticket {ticket_id}")
            except Exception as e:
                logger.error(f"[ENDPOINT] ❌ Failed to send Slack notification: {str(e)}")
        
        return {
            "status": "success",
            "ticket_id": ticket_id,
            "analysis": result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error analyzing ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing ticket: {str(e)}")
