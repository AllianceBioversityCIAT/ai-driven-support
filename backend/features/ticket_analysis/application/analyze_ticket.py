"""
Analyze Ticket Use Case
Orchestrates ticket analysis workflow
"""
import logging
from typing import Dict, Any
from datetime import datetime
from ..domain.entities import TicketAnalysisResult, TicketData

logger = logging.getLogger(__name__)


class AnalyzeTicketUseCase:
    """Use case for analyzing a single ticket"""
    
    def __init__(self, ai_analyzer):
        self.ai_analyzer = ai_analyzer
    
    def execute(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute ticket analysis
        
        Args:
            ticket_data: Raw ticket data from external source
            
        Returns:
            Analysis result dictionary
        """
        logger.info(f"[USE_CASE] Analyzing ticket {ticket_data.get('id')}")
        
        # Delegate to AI analyzer service
        result = self.ai_analyzer.analyze_ticket(ticket_data)
        
        return result
