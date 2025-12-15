"""
Ticket Management Domain Entities
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Ticket:
    """Core ticket entity"""
    id: str
    subject: str
    description: str
    status: str
    priority: str
    requester_id: Optional[int] = None
    group_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class TicketConversation:
    """Ticket conversation entity"""
    id: str
    ticket_id: str
    body: str
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None


@dataclass
class TicketSearchCriteria:
    """Search criteria for tickets"""
    query: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    group_id: Optional[int] = None
    page: int = 1
    per_page: int = 30
