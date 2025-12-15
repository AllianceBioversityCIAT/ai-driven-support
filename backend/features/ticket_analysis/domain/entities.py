"""
Ticket Analysis Domain Entities
Core business objects for ticket analysis
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class TicketAnalysisResult:
    """Analysis result for a support ticket"""
    ticket_id: str
    summary: str
    possible_categories: List[dict]
    possible_automations: List[dict]
    user_sentiment: dict
    analyzed_at: datetime


@dataclass
class TicketData:
    """Ticket domain entity"""
    id: str
    subject: str
    description: str
    description_text: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
