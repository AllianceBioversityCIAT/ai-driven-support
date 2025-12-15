"""
List Tickets Use Case
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ListTicketsUseCase:
    """Use case for listing tickets with pagination"""
    
    def __init__(self, freshservice_client):
        self.client = freshservice_client
    
    def execute(self, page: int = 1, per_page: int = 30, group_id: int = None) -> Dict[str, Any]:
        """
        Execute ticket listing
        
        Args:
            page: Page number
            per_page: Items per page
            group_id: Optional group filter
            
        Returns:
            Paginated ticket list
        """
        logger.info(f"[USE_CASE] Listing tickets: page={page}, per_page={per_page}, group_id={group_id}")
        
        result = self.client.get_tickets(page=page, per_page=per_page, group_id=group_id)
        
        return {
            "tickets": result.get("tickets", []),
            "pagination": {
                "page": result.get("page"),
                "per_page": result.get("per_page"),
                "total": result.get("total"),
                "has_more": result.get("has_more")
            }
        }
