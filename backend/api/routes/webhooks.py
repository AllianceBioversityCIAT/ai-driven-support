"""
Webhook Endpoints for FreshService
Receives and processes webhook events from FreshService
"""
import logging
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from typing import Dict, Any
from config import config
from api.freshservice_client import FreshServiceClient
from services.ai_analyzer import TicketAnalyzer
from infrastructure.notifications import SlackNotificationService

logger = logging.getLogger(__name__)

router = APIRouter()


async def analyze_ticket_background(ticket_id: str, group_id: int):
    """
    Background task to analyze ticket and send to Slack
    
    Args:
        ticket_id: Ticket ID to analyze
        group_id: Group ID that owns the ticket
    """
    try:
        logger.info(f"[WEBHOOK] 🤖 Starting background analysis for ticket {ticket_id} (group {group_id})")
        
        # Get FreshService client
        client = FreshServiceClient(
            api_key=config.FRESHSERVICE_API_KEY,
            domain=config.FRESHSERVICE_DOMAIN
        )
        
        # Fetch ticket details
        ticket = client.get_ticket(ticket_id)
        
        if not ticket:
            logger.error(f"[WEBHOOK] ❌ Ticket {ticket_id} not found")
            return
        
        # Analyze ticket
        analyzer = TicketAnalyzer()
        analysis = analyzer.analyze_ticket(ticket)
        
        if analysis.get("status") != "success":
            logger.error(f"[WEBHOOK] ❌ Analysis failed for ticket {ticket_id}: {analysis.get('message')}")
            return
        
        logger.info(f"[WEBHOOK] ✅ Analysis completed for ticket {ticket_id}")
        
        # Send to Slack if configured
        if config.SLACK_WEBHOOK_URL:
            slack_service = SlackNotificationService(config.SLACK_WEBHOOK_URL)
            success = slack_service.send_ticket_analysis(
                ticket_id, 
                analysis["analysis"],
                domain=config.FRESHSERVICE_DOMAIN
            )
            
            if success:
                logger.info(f"[WEBHOOK] 📨 Slack notification sent for ticket {ticket_id}")
            else:
                logger.error(f"[WEBHOOK] ❌ Failed to send Slack notification for ticket {ticket_id}")
        else:
            logger.warning(f"[WEBHOOK] ⚠️ Slack webhook not configured, skipping notification")
            
    except Exception as e:
        logger.error(f"[WEBHOOK] ❌ Error in background analysis: {str(e)}")


@router.post("/freshservice/ticket-created")
async def ticket_created_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook endpoint for FreshService ticket created events
    
    FreshService will POST to this endpoint when a ticket is created
    """
    try:
        # Get webhook payload
        payload = await request.json()
        
        logger.info(f"[WEBHOOK] 📥 Received ticket created event")
        logger.debug(f"[WEBHOOK] Payload: {payload}")
        
        # Extract ticket data
        ticket_data = payload.get("ticket_changes", {})
        ticket_id = ticket_data.get("id")
        group_id = ticket_data.get("group_id")
        
        if not ticket_id:
            logger.error(f"[WEBHOOK] ❌ No ticket ID in payload")
            return {"status": "error", "message": "No ticket ID found"}
        
        logger.info(f"[WEBHOOK] Ticket ID: {ticket_id}, Group ID: {group_id}")
        
        # Check if ticket belongs to configured groups
        if group_id and config.AUTO_ANALYZE_GROUP_IDS:
            group_id_str = str(group_id)
            configured_groups = [g.strip() for g in config.AUTO_ANALYZE_GROUP_IDS if g.strip()]
            
            if group_id_str not in configured_groups:
                logger.info(f"[WEBHOOK] ⏭️ Group {group_id} not in configured list {configured_groups}, skipping")
                return {"status": "ok", "message": f"Group {group_id} not configured for analysis"}
        
        # Add analysis task to background
        background_tasks.add_task(analyze_ticket_background, ticket_id, group_id)
        
        logger.info(f"[WEBHOOK] ✅ Analysis task queued for ticket {ticket_id}")
        
        return {
            "status": "ok",
            "message": f"Analysis queued for ticket {ticket_id}",
            "ticket_id": ticket_id,
            "group_id": group_id
        }
        
    except Exception as e:
        logger.error(f"[WEBHOOK] ❌ Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/freshservice/ticket-updated")
async def ticket_updated_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook endpoint for FreshService ticket updated events
    
    Optional: Can be used to re-analyze tickets when they're updated
    """
    try:
        payload = await request.json()
        
        logger.info(f"[WEBHOOK] 📥 Received ticket updated event")
        
        # For now, just log the update
        ticket_data = payload.get("ticket_changes", {})
        ticket_id = ticket_data.get("id")
        
        logger.info(f"[WEBHOOK] Ticket {ticket_id} updated (no action taken)")
        
        return {"status": "ok", "message": "Update acknowledged"}
        
    except Exception as e:
        logger.error(f"[WEBHOOK] ❌ Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/webhooks/test")
async def test_webhook():
    """Test endpoint to verify webhooks are working"""
    return {
        "status": "ok",
        "message": "Webhook endpoint is active",
        "mode": "webhook_only",
        "monitored_groups": config.AUTO_ANALYZE_GROUP_IDS,
        "slack_configured": bool(config.SLACK_WEBHOOK_URL),
        "note": "Configure FreshService automation to call /api/webhooks/freshservice/ticket-created"
    }


@router.post("/webhooks/test-analysis/{ticket_id}")
async def test_ticket_analysis(ticket_id: str, background_tasks: BackgroundTasks):
    """
    Manual test endpoint to trigger analysis for a specific ticket
    Useful for testing without setting up FreshService webhooks
    """
    logger.info(f"[WEBHOOK] 🧪 Manual test analysis triggered for ticket {ticket_id}")
    
    background_tasks.add_task(analyze_ticket_background, ticket_id, None)
    
    return {
        "status": "ok",
        "message": f"Test analysis queued for ticket {ticket_id}",
        "note": "Check backend logs and Slack for results"
    }


@router.get("/freshservice/groups")
async def list_groups():
    """
    List all FreshService groups
    Helps identify group IDs for auto-analysis configuration
    """
    try:
        client = FreshServiceClient(
            api_key=config.FRESHSERVICE_API_KEY,
            domain=config.FRESHSERVICE_DOMAIN
        )
        
        groups = client.get_groups()
        
        return {
            "status": "ok",
            "groups": groups,
            "total": len(groups),
            "note": "Use the 'id' field to configure AUTO_ANALYZE_GROUP_IDS in .env"
        }
        
    except Exception as e:
        logger.error(f"[GROUPS] Error fetching groups: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
