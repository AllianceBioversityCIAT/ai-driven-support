"""
Ticket routes for FreshAI API
"""
import logging
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
from config import config
from api.freshservice_client import FreshServiceClient
from services.ai_analyzer import TicketAnalyzer

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize clients
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


@router.get("/")
async def list_tickets(
    page: int = Query(1, ge=1),
    per_page: int = Query(30, ge=1, le=100),
    group_id: Optional[int] = Query(None)
):
    """Get list of tickets with pagination and optional group filtering"""
    logger.info(f"📋 Fetching tickets: page={page}, per_page={per_page}, group_id={group_id}")
    try:
        client = get_fs_client()
        result = client.get_tickets(page=page, per_page=per_page, group_id=group_id)
        return {
            "status": "success",
            "data": {
                "tickets": result.get("tickets", []),
                "pagination": {
                    "page": result.get("page"),
                    "per_page": result.get("per_page"),
                    "total": result.get("total"),
                    "has_more": result.get("has_more")
                }
            }
        }
    except Exception as e:
        logger.error(f"❌ Error fetching tickets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching tickets: {str(e)}")


@router.get("/{ticket_id}")
async def get_ticket(ticket_id: str, include_conversations: bool = False):
    """Get single ticket by ID"""
    logger.info(f"🎫 Fetching ticket: {ticket_id}")
    try:
        client = get_fs_client()
        ticket = client.get_ticket(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        if include_conversations:
            conversations = client.get_ticket_conversations(ticket_id)
            ticket['conversations'] = conversations

        return {
            "status": "success",
            "ticket": ticket
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error fetching ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching ticket: {str(e)}")


@router.get("/{ticket_id}/summary")
async def get_ticket_summary(ticket_id: str):
    """Get ticket summary"""
    logger.info(f"📄 Getting summary for ticket: {ticket_id}")
    try:
        client = get_fs_client()
        ticket = client.get_ticket(ticket_id)
        
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return {
            "status": "success",
            "ticket_id": ticket_id,
            "subject": ticket.get("subject", ""),
            "description": ticket.get("description", "")[:500]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting summary: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting summary: {str(e)}")


@router.get("/{ticket_id}/conversations")
async def get_ticket_conversations_detail(ticket_id: str):
    """Get ticket conversations"""
    logger.info(f"💬 Getting conversations for ticket: {ticket_id}")
    try:
        client = get_fs_client()
        conversations = client.get_ticket_conversations(ticket_id)
        
        return {
            "status": "success",
            "ticket_id": ticket_id,
            "conversations": conversations,
            "total": len(conversations)
        }
    except Exception as e:
        logger.error(f"❌ Error getting conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting conversations: {str(e)}")


@router.get("/search/tickets")
async def search_tickets(query: str = Query(..., min_length=1)):
    """Search tickets"""
    logger.info(f"🔍 Searching tickets: {query}")
    try:
        client = get_fs_client()
        results = client.search_tickets(query)
        return {
            "status": "success",
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        logger.error(f"❌ Error searching tickets: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error searching tickets: {str(e)}")

@router.post("/{ticket_id}/analyze")
async def analyze_ticket(ticket_id: str):
    """Analyze a single ticket with AI"""
    logger.info(f"🤖 Analyzing ticket: {ticket_id}")
    try:
        client = get_fs_client()
        ticket = client.get_ticket(ticket_id)

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        # Initialize AI analyzer
        analyzer = TicketAnalyzer()
        analysis = analyzer.analyze_ticket(ticket)

        return {
            "status": "success",
            "ticket_id": ticket_id,
            "analysis": analysis
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error analyzing ticket: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing ticket: {str(e)}")
