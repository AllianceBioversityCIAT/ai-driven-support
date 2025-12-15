"""
Search Tickets Use Case
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class SearchTicketsUseCase:
    """Use case for searching tickets"""
    
    def __init__(self, freshservice_client):
        self.client = freshservice_client
    
    def execute(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute ticket search
        
        Args:
            query: Search query
            
        Returns:
            List of matching tickets
        """
        logger.info(f"[USE_CASE] Searching tickets: {query}")
        
        results = self.client.search_tickets(query)
        
        return results
