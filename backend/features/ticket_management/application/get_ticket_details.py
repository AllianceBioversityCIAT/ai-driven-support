"""
Get Ticket Details Use Case
"""
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class GetTicketDetailsUseCase:
    """Use case for getting ticket details"""
    
    def __init__(self, freshservice_client):
        self.client = freshservice_client
    
    def execute(self, ticket_id: str, include_conversations: bool = False) -> Optional[Dict[str, Any]]:
        """
        Execute get ticket details
        
        Args:
            ticket_id: Ticket ID
            include_conversations: Whether to include conversations
            
        Returns:
            Ticket details or None if not found
        """
        logger.info(f"[USE_CASE] Getting ticket details: {ticket_id}")
        
        ticket = self.client.get_ticket(ticket_id)
        
        if not ticket:
            return None
        
        if include_conversations:
            conversations = self.client.get_ticket_conversations(ticket_id)
            ticket['conversations'] = conversations
        
        return ticket
